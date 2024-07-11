import sys, cv2, argparse, pathlib, os
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

def detect_blobs(image_path, output_path, region):
    input_path = str(image_path.resolve())
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    x, y, w, h = region
    cropped_img = img[y:y+h, x:x+w]
    cv2.imwrite(f"{output_path}{os.sep}path.png", cropped_img)
    detector = setup_detector(min_area=100, max_area=2000, circularity=0.1, 
                              convexity=0.01, inertia=0.01)
    dilated = prepare_image(cropped_img)
    # Detect blobs using the detector
    keypoints = detector.detect(dilated)

    # Draw detected blobs as red circles
    colour = (0,0,255)
    flag_match = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    img_with_keypoints = cv2.drawKeypoints(cropped_img, keypoints, np.array([]), 
                                           colour, flag_match)
    cv2.imwrite(f"{output_path}{os.sep}path_blobs.png", img_with_keypoints)
    print("Process complete", flush=True)

def prepare_image(image):
    adap_thresh = cv2.adaptiveThreshold(image, 255, 
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 17, 0)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    return cv2.dilate(adap_thresh, element, iterations=1)   

def setup_detector(min_area, max_area, circularity, convexity, inertia):
    params = cv2.SimpleBlobDetector_Params()
    # Set up the detector parameters
    params.filterByColor = 1
    params.blobColor = 255
    params.filterByArea = True
    params.minArea = min_area
    params.maxArea = max_area
    params.filterByCircularity = True
    params.minCircularity = circularity
    params.filterByConvexity = True
    params.minConvexity = convexity
    params.filterByInertia = True
    params.minInertiaRatio = inertia
    
    return cv2.SimpleBlobDetector_create(params)

def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
        usage="%(prog)s [-h] [-v] -i INPUT_PATH -o OUTPUT_PATH -r ROI", add_help=False, 
        description="Detect blobs of an image and output image of blobs circled."
    )

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--infile", action="store", type=pathlib.Path,
                          required=True, help = "Full path to compacted frames file")
    required.add_argument("-o", "--outdir", action="store", type=pathlib.Path,
                          required=True, help = "Full path to output directory")
    required.add_argument("-r", "--region", action="store", type=tuple_type,
                          required=True, help = "Region where the path is in form: (x, y, w, h)")

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-h", "--help", action="help", 
                          help="show this help message and exit")
    optional.add_argument("-v", "--version", action="version", 
                        version=f"{parser.prog} version 1.0.0")
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        detect_blobs(args.infile, args.outdir, args.region)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()