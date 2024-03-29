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
    

def combine_images(input_path, output_path):
    '''Takes frames and computes difference between them, and combines these differences into one image.

    Parameters:
        video_path(str): Path to frames.
        output_path(str): Path to dir to output difference frames.       
    '''
    input_abs_path = input_path[0].resolve()
    output_abs_path = output_path[0].resolve()
    count = len(os.listdir(input_abs_path))
    if count < 1:
        raise IOError("Frames folder is empty")
        
    if os.path.exists(output_abs_path):
        if not is_dir_empty(output_abs_path):
            raise IOError(f"Files already exist in {output_abs_path}")
    else:
        raise FileNotFoundError(f"{output_abs_path} does not exist")
    
    for i in range(count - 2): #control how many frames
        img1 = cv.imread(f"{input_abs_path}/{str(i).zfill(4)}.jpg")
        img2 = cv.imread(f"{input_abs_path}/{str(i+1).zfill(4)}.jpg")
        difference = cv.absdiff(img1, img2)

        greyscaled = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
        ret, mask = cv.threshold(greyscaled, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        difference[mask != 255] = [0, 0, 255] #might want to make a parmater
        cv.imwrite(f"{output_abs_path}/diff{i}.png", difference)
        
    img = cv.imread(f"{output_abs_path}/diff0.png", 0)
    for x in range(count - 3):
        img_name = f"{output_abs_path}/diff{x}.png"
        print('Processing:', img_name)
        nxt = cv.imread(img_name, 0)
        for i, row in enumerate(img):
            for j, pixel in enumerate(row):
                d = int(img[i][j]) - int(nxt[i][j])
                if abs(d) > 15: #2 successive frames, mayeb another tool to calc 
                    img[i][j] = 255
                else:
                    img[i][j] = (int(img[i][j]) + int(nxt[i][j]))/2
        os.remove(f"{output_abs_path}/diff{x}.png")
    os.remove(f"{output_abs_path}/diff{max(range(count- 2))}.png")

    for i, row in enumerate(img):
        for j, pixel in enumerate(row):
            if img[i][j] < 255:
                img[i][j] = 0
    cv.imwrite(f"{output_abs_path}/final.png", img)
    print("Image processing sucessful")

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [[-v|--version] | [-h|--help]] | [-i|--indir <input-file-path> -o|--outdir <output-file-path>]",
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
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        combine_images(args.indir, args.outdir)
    except Exception as err:
        print(err)
        exit(1)
        
if __name__ == "__main__":
    main()
