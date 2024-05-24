import sys, os
import pathlib
import cv2
from PIL import Image
import argparse

def calculate_threshold(image1_path, image2_path, dimensionX, dimensionY):
    input_path1 = image1_path[0].resolve()
    input_path1 = str(input_path1)
    img1 = cv2.imread(input_path1, cv2.IMREAD_GRAYSCALE)

    input_path2 = image2_path[0].resolve()
    input_path2 = str(input_path2)
    img2 = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)

    x1 = dimensionX[0]
    x2 = dimensionX[1]
    y1 = dimensionY[0]
    y2 = dimensionY[1]

    differences = []

    for xi in range(x1, x2):
        for yi in range(y1, y2):
            first_frame_area = int(img1[yi][xi])
            second_frame_area = int(img2[yi][xi])
            diff = abs(first_frame_area-second_frame_area)
            differences.append(diff)

    threshold = sum(differences)/len(differences)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [[-v|--version] | [-h|--help]] | [-i|--infile <input-file-path>] | [-i|--infile <input-file-path>] |  [-i|--infile <input-file-path>] |  [-i|--infile <input-file-path>]",
        description="Converts mp4 video into photo"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-i", "--infile1", action="store", nargs=1, type=pathlib.Path,
        help = "Full path to first frame"
    )
    parser.add_argument(
        "-i", "--infile2", action="store", nargs=1, type=pathlib.Path,
        help = "Full path to second frame"
    )
    parser.add_argument(
        "-x", "--dimensionX", action="store", nargs=1, type=tuple,
        help = "X dimensions used in calculation"
    )
    parser.add_argument(
        "-y", "--dimensionY", action="store", nargs=1, type=tuple,
        help = "Y dimensions used in calculation"
    )
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        calculate_threshold(args.infile1, args.infile2, args.dimensionX, args.dimensionY)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()