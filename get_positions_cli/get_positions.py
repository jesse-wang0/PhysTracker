import cv2, os, argparse, pathlib, sys, csv
from tabulate import tabulate

current_directory = os.path.dirname(sys.path[0])
if current_directory not in sys.path:
    sys.path.append(current_directory)
from blob_detection_cli.blob_detection import setup_detector

def get_positions(frames_path, frame_duration, roi, scale,
                  avg_file_name="average.jpg", queue=None):
    avg_background_path = str(frames_path.resolve()) + os.sep + avg_file_name
    average_background = cv2.imread(avg_background_path)
    input_path = str(frames_path.resolve())
    img_paths = os.listdir(input_path)

    x_coords = []
    y_coords = []
    image_height = average_background.shape[0]

    count = 0
    for path in img_paths:
        name, ext = os.path.splitext(path)
        if ext.lower() not in ('.jpg', '.png'):
            continue
        img = cv2.imread(f"{input_path}{os.sep}{path}")
        difference = cv2.absdiff(img, average_background)
        difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        f_, thresholded_diff = cv2.threshold(difference, 15, 255, 
                                             cv2.THRESH_BINARY)

        detector = setup_detector(min_area=200, max_area=2000, circularity=0.3, 
                                  convexity=0.1, inertia=0.01)
        keypoints = detector.detect(thresholded_diff)

        max_area = 0
        max_area_point = None
        for key_point in keypoints:
            x = key_point.pt[0]
            y = key_point.pt[1]
            size = key_point.size

            roi_x = roi[0]
            roi_y = roi[1]
            roi_w = roi[2]
            roi_h = roi[3]

            if (roi_x < x < roi_x + roi_w) and (roi_y < y < roi_y + roi_h):
                if size > max_area:
                    max_area_point = key_point
        if max_area_point is not None:
            x_coords.append(max_area_point.pt[0] * scale)
            y_coords.append((image_height - max_area_point.pt[1]) * scale)
            progress_msg = f"Progress: {count}/{len(img_paths) - 1}"
            if queue is not None:
                queue.put(progress_msg)
            print(progress_msg, flush=True)
        count += 1

    header = ["Time (seconds)", "x (meters)", "y (meters)"]
    rows = []

    for i in range(len(x_coords)):
        rows.append([i * frame_duration, x_coords[i], y_coords[i]])

    table = tabulate(rows, header, tablefmt="grid")
    print(table, file=sys.stdout)

    output_path = f"{input_path}{os.sep}data"
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    with open(f"{output_path}{os.sep}position_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Time", "x", "y"])
        writer.writerows(rows)
    if queue is not None:
        queue.put("Process successful")
    print("Process successful", flush=True)
    
def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
        usage="%(prog)s [-h] [-v] -i INPUT_PATH -f frame_duration -r ROI -m M_PER_PIXEL", 
        add_help=False, description="Converts mp4 video into photo")

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--inpath", action="store", type=pathlib.Path, 
                          required=True, help = "Full path to directory containing frames")
    required.add_argument("-d", "--duration_frame", action="store", type=float,
                          required=True, help = "Duration of time apart of each frame in seconds")
    required.add_argument("-r", "--roi", action="store", type=tuple_type,
                          required=True, help = "Region of interest coordinates as tuple (x,y,w,h)")
    required.add_argument("-m", "--meter_per_pixel", action="store", type=float, 
                          required=True, help = "Meter per pixel conversion factor")

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-h", "--help", action="help", 
                          help="show this help message and exit")
    optional.add_argument("-v", "--version", action="version", 
                        version=f"{parser.prog} version 1.0.0")
    optional.add_argument("-a", "--avg_img", action="store", type=str, 
                          default="average.jpg",
                          help = "Name of average image that will be used as base comparison")
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        get_positions(args.inpath, args.duration_frame, 
                      args.roi, args.meter_per_pixel, args.avg_img)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()