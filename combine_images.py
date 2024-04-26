import sys, os
import argparse
import pathlib
import cv2 as cv
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
    

def combine_images(input_path, output_path, force_flag):
    '''Takes frames and computes difference between them, and combines these differences into one image.

    Parameters:
        video_path(str): Path to frames.
        output_path(str): Path to dir to output difference frames.       
    '''
    input_abs_path = input_path[0].resolve()
    output_abs_path = output_path[0].resolve()
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
        img1 = cv.imread(f"{input_abs_path}/{img_files[i]}")
        img2 = cv.imread(f"{input_abs_path}/{img_files[i+1]}")
        difference = cv.absdiff(img1, img2)

        greyscaled = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
        ret, mask = cv.threshold(greyscaled, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        difference[mask != 255] = [0, 0, 255] #might want to make a parmater
        cv.imwrite(f"{output_abs_path}/diff{i}.png", difference)
    
    img = cv.imread(f"{output_abs_path}/diff0.png", 0)
    
    total_list = []
    for x in range(0, len(img_files)-1): 
        list_trial = []
        img_name = f"{output_abs_path}/diff{x}.png"
        print('Processing:', img_name)
        nxt = cv.imread(img_name, 0)
        for i, row in enumerate(img):
            for j, pixel in enumerate(row):
                d = int(img[i][j]) - int(nxt[i][j])
                if abs(d) > 60: #2 successive frames, mayeb another tool to calc
                    img[i][j] = 255
                    list_trial.append((i,j))
                else:
                    img[i][j] = (int(img[i][j]) + int(nxt[i][j]))/2
        os.remove(f"{output_abs_path}/diff{x}.png")

    for i, row in enumerate(img):
        for j, pixel in enumerate(row):
            if img[i][j] < 255:
                img[i][j] = 0
    cv.imwrite(f"{output_abs_path}/final.png", img)
    print("Image processing sucessful")

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="""%(prog)s [[-v|--version] | [-h|--help]] 
        | [-i|--indir <input-file-path> -o|--outdir <output-file-path>] 
        | [-f|--force]""",
        description="Takes frames and combines them into one photo"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-i", "--indir", action="store", nargs=1, type=pathlib.Path,
        help = "Full path to directory containing frames"
    )
    parser.add_argument(
        "-o", "--outdir", action="store", nargs=1, type=pathlib.Path,
        help = "Directory to store image differences."
    )   
    parser.add_argument(
        "-f", "--force", action=argparse.BooleanOptionalAction, type=bool,
        help = "Force writes to directory with pre-existing files and overwrites old files."
    )
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        combine_images(args.indir, args.outdir, args.force)
        exit(0)
    except Exception as err:
        print(err)
        exit(1)

if __name__ == "__main__":
    main()
