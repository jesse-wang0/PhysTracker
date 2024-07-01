import sys, pathlib, cv2, argparse, math

def calculate_threshold(image1_path, image2_path, dimensionX, dimensionY):
    input_path1 = str(image1_path.resolve())
    img1 = cv2.imread(input_path1, cv2.IMREAD_GRAYSCALE)
    
    input_path2 = str(image2_path.resolve())
    img2 = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)

    if dimensionX and dimensionY:
        col_start, col_end = dimensionX
        row_start, row_end = dimensionY
    else:
        x, y, w, h = cv2.selectROI(img1)
        cv2.destroyAllWindows()
        col_start = x
        col_end = x + w
        row_start = y
        row_end = y + h

    differences = []
    for column in range(min(col_start, col_end), max(col_start, col_end)):
        for row in range(min(row_start, row_end), max(row_start, row_end)):
            first_frame_area = int(img1[row][column])
            second_frame_area = int(img2[row][column])
            diff = abs(first_frame_area - second_frame_area)
            differences.append(diff)

    print(f"Threshold Amount: {math.ceil(sum(differences)/len(differences))}")
    return math.ceil(sum(differences)/len(differences))

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
         usage=(
             "%(prog)s [-h] [-v] "
             "| [-i|--infile <input-file-path>] "
             "| [-j|--infile <input-file-path>] "
             "|  [-x|--x-dimension <x-dimension> -y|--y-dimension <y-dimension>]"
        ),
        description="Calculates threshold value used in combine_images based off regions of 2 frames. Note: Both -x and -y must be provided together or not at all."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-i", "--infile1", action="store", type=pathlib.Path, required=True,
        help = "Full path to first frame"
    )
    parser.add_argument(
        "-j", "--infile2", action="store", type=pathlib.Path, required=True,
        help = "Full path to second frame"
    )
    parser.add_argument(
        "-x", "--dimensionX", type=tuple_type,
        help = "X dimensions used in calculation"
    )
    parser.add_argument(
        "-y", "--dimensionY", type=tuple_type,
        help = "Y dimensions used in calculation"
    )
    return parser


def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if (args.dimensionX is None) != (args.dimensionY is None):
        parser.error("Both --dimension1 and --dimension2 must be provided together or not at all.")
        
    try:
        calculate_threshold(args.infile1, args.infile2, args.dimensionX, 
                            args.dimensionY)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()