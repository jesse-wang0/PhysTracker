import cv2, os, argparse, pathlib, sys
from tabulate import tabulate
from blob_detection import setup_detector

def get_positions(frames_path, avg_img_path, frame_duration, 
                  roi, meters_per_pixel):
    avg_background_path = str(avg_img_path.resolve())
    average_background = cv2.imread(avg_background_path)
    input_path = str(frames_path.resolve())
    img_paths = os.listdir(input_path)

    x_coords = []
    y_coords = []
    image_height = average_background.shape[0]

    for path in img_paths:
        img = cv2.imread(f"{input_path}/{path}")
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

            x1 = roi[0]
            x2 = roi[1]
            y1 = roi[2]
            y2 = roi[3]
            if x1 < x < x2 and y1 < y < y2:
                if size > max_area:
                    max_area_point = key_point
        if max_area_point is not None:
            x_coords.append(max_area_point.pt[0] * meters_per_pixel)
            y_coords.append((image_height - max_area_point.pt[1]) 
                             * meters_per_pixel)
    
    headers = ["Time (seconds)", "x (meters)", "y (meters)"]
    rows = []
    #just used x_coords, as both x and y lists are same size
    for i in range(len(x_coords)): 
        rows.append([i*frame_duration, x_coords[i], y_coords[i]])
    table = tabulate(rows, headers, tablefmt="grid")
    print(table)

def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage=(
            "%(prog)s [[-v|--version] | [-h|--help]] "
            "| [-i|--infile <input-file-path>]"
        ),
        description="Converts mp4 video into photo"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-i", "--indir", action="store", type=pathlib.Path,
        help = "Full path to input directory containing compacted frames"
    )
    parser.add_argument(
        "-a", "--avg_img", action="store", type=pathlib.Path,
        help = "Full path to average image that will be used as base comparison"
    )
    parser.add_argument(
        "-d", "--duration_frame", action="store", type=float,
        help = "Duration of time apart of each frame in seconds"
    )
    parser.add_argument(
        "-r", "--roi", action="store", type=tuple_type,
        help = "Region of interest coordinates as tuple (x1, x2, y1, y2)"
    )
    parser.add_argument(
        "-m", "--meter_per_pixel", action="store", type=float,
        help = "Meter per pixel conversion factor"
    )
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        get_positions(args.indir, args.avg_img, args.duration_frame, 
                      args.roi, args.meter_per_pixel)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()