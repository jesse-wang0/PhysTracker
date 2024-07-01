import sys, cv2, argparse, pathlib
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

def detect_blobs(image_path):
    input_path = str(image_path.resolve())
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    image_height = img.shape[0]
    detector = setup_detector(min_area=100, max_area=2000, circularity=0.1, 
                              convexity=0.01, inertia=0.01)
    dilated = prepare_image(img)
    # Detect blobs using the detector
    keypoints = detector.detect(dilated)

    x_coords = np.zeros(len(keypoints))
    y_coords = np.zeros(len(keypoints))
    count = 0
    for key_point in keypoints:
        x = key_point.pt[0]
        y = key_point.pt[1]
        s = key_point.size
        x_coords[count] = x
        y_coords[count] = image_height - y
        count += 1

    plt.plot(x_coords, y_coords, 'o')
    plt.show()

    # Draw detected blobs as red circles
    colour = (0,0,255)
    flag_match = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), 
                                           colour, flag_match)
    cv2.imwrite(f"final.png", img_with_keypoints)

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

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
        usage="%(prog)s [-h] [-v] -i INPUT_PATH", add_help=False, 
        description="Detect blobs of an image and output image of blobs circled."
    )

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--infile", action="store", type=pathlib.Path,
                          required=True, help = "Full path to compacted frames file")

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
        detect_blobs(args.infile)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()