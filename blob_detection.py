import sys, os
import cv2
import numpy as np
import argparse
import pathlib

def detect_blobs(image_path):
    input_path = image_path[0].resolve()
    input_path = str(input_path)

    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.medianBlur(img, 5)
    adap_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 17, 0)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(adap_thresh, element, iterations=1)

    # Create SimpleBlobDetector object with default parameters
    params = cv2.SimpleBlobDetector_Params()

    # Set up the detector parameters
    params.filterByColor = 1
    params.blobColor = 255
    params.filterByArea = True
    params.minArea = 200
    params.filterByCircularity = True
    params.minCircularity = 0.1
    params.filterByConvexity = True
    params.minConvexity = 0.2
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    # Detect blobs using the detector
    keypoints = detector.detect(dilated)
    # Draw detected blobs as red circles
    img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite(f"final.png", img_with_keypoints)



def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [[-v|--version] | [-h|--help]] | [-i|--infile <input-file-path>]",
        description="Converts mp4 video into photo"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-i", "--infile", action="store", nargs=1, type=pathlib.Path,
        help = "Full path to compacted frames file"
    )
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