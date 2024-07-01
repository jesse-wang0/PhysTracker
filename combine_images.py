import sys, os
import argparse
import pathlib
import cv2
from PIL import Image

def is_dir_empty(path):
    '''Checks if directory provided is empty

    Parameters:
        path(str): Path to directory that will be checked.
        
    Return:
        bool: True if dir emtpy, False otherwise.
        
    '''
    with os.scandir(path) as scan:
        return next(scan, None) is None
    

def combine_images(input_path, output_path, threshold, force_flag):
    """Takes frames and computes difference between them, and 
    combines these differences into one image.

    Parameters:
        video_path(str): Path to frames.
        output_path(str): Path to dir to output difference frames.       
    """
    input_abs_path = input_path.resolve()
    output_abs_path = output_path.resolve()

    img_files = os.listdir(input_abs_path)
    if len(img_files) < 1:
        raise IOError("Frames folder is empty")
        
    if os.path.exists(output_abs_path):
        if not force_flag:
            if not is_dir_empty(output_abs_path):
                raise IOError(f"Files already exist in {output_abs_path}.")
    else:
        raise FileNotFoundError(f"{output_abs_path} does not exist.")

    for i in range(0, len(img_files)-1):
        img1 = cv2.imread(f"{input_abs_path}{os.sep}{img_files[i]}")
        img2 = cv2.imread(f"{input_abs_path}{os.sep}{img_files[i+1]}")

        difference = cv2.absdiff(img1, img2)
        cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f"{output_abs_path}{os.sep}diff{i}.png", difference)

    img = cv2.imread(f"{output_abs_path}{os.sep}diff0.png", 0)
    
    for x in range(0, len(img_files)-1): 
        list_trial = []
        img_name = f"{output_abs_path}{os.sep}diff{x}.png"
        print("Processing: ", img_name)
        nxt = cv2.imread(img_name, 0)
        for i, row in enumerate(img):
            for j, pixel in enumerate(row):
                d = int(img[i][j]) - int(nxt[i][j])
                if abs(d) > threshold:
                    img[i][j] = 255
                    list_trial.append((i,j))
                else:
                    img[i][j] = (int(img[i][j]) + int(nxt[i][j]))/2
        os.remove(f"{output_abs_path}/diff{x}.png")

    for i, row in enumerate(img):
        for j, pixel in enumerate(row):
            if img[i][j] < 255:
                img[i][j] = 0
    cv2.imwrite(f"{output_abs_path}{os.sep}final.png", img)
    print("Image processing sucessful")

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
        usage="%(prog)s [-h] [-v] -i INPUT_PATH -o OUTPUT_PATH -t THRESHOLD [-f]", 
        add_help=False, description="Given input path containing frames, combines them into an image mask"
    )

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--infile", action="store", type=pathlib.Path, 
                          required=True, help = "Full path to directory containing frames")
    required.add_argument("-o", "--outdir", action="store", type=pathlib.Path, 
                          required=True, help = "Directory to store final result")
    required.add_argument("-t", "--threshold", action="store", default="1", type=int, 
                          required=True, help = "Threshold value calculated by threshold tool")

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-h", "--help", action="help", 
                          help="show this help message and exit")
    optional.add_argument("-v", "--version", action="version", 
                        version=f"{parser.prog} version 1.0.0")
    optional.add_argument("-f", "--force", action=argparse.BooleanOptionalAction, \
                        type=bool, help = """Force writes to directory with pre-existing files \
                    and overwrites old files.""")
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        combine_images(args.indir, args.outdir, args.threshold, args.force)
        exit(0)
    except Exception as err:
        print(err)
        exit(1)

if __name__ == "__main__":
    main()