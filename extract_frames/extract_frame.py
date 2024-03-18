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
    
def to_image(video_path, output_path):
    '''Converts mp4 video into individual frames and stores in provided output path.

    Parameters:
        video_path(str): Path to video.
        output_path(str): Path to output dir.       
    '''
    input_abs_path = video_path[0].resolve()
    output_abs_path = output_path[0].resolve()
    if not str(input_abs_path).endswith(".mp4"):
        raise TypeError(f"Input is not an mp4 file")
    
    vid = cv.VideoCapture(str(input_abs_path))
    read_success, image = vid.read()
    if not read_success:
        raise IOError(f"Couldn't read from {input_abs_path}")
    if os.path.exists(output_abs_path):
        if not is_dir_empty(output_abs_path):
            raise IOError(f"Files already exist in {output_abs_path}")
    else:
        raise FileNotFoundError(f"{output_abs_path} does not exist")
    
    count = 0
    while read_success:
        write_path = f"{output_abs_path}/{str(count).zfill(4)}.jpg"
        write_success = cv.imwrite(write_path, image) # save frame as JPEG file
        if not write_success:
            raise IOError(f"Couldn't write to {write_path}")
        read_success, image = vid.read()
        print('Read a new frame: ', read_success)
        count += 1

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [[-v|--version] | [-h|--help]] | [-i|--infile <input-file-path> -o|--outdir <output-file-path>]",
        description="Converts mp4 video into photo"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-i", "--infile", action="store", nargs=1, type=pathlib.Path,
        help = "Full path to an mp4 file"
    )
    parser.add_argument(
        "-o", "--outdir", action="store", nargs=1, type=pathlib.Path,
        help = "Empty directory to store frames in. Output = nnnn.jpg and starts from 0000 onwards"
    )
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        to_image(args.infile, args.outdir)
    except Exception as err:
        print(err)
        exit(1)
        
if __name__ == "__main__":
    main()
