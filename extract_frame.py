import sys, os, argparse, pathlib, cv2
from PIL import Image
from io import BytesIO

class ExtractFrameException(Exception):
    pass

def get_first_image(path):
        vidcap = cv2.VideoCapture(path)
        success, image = vidcap.read()
        if success:
            return Image.open(BytesIO(image))

def is_dir_empty(path):
    '''Checks if directory provided is empty.

    Parameters:
        path(str): Path to directory that will be checked.
        
    Return:
        bool: True if dir emtpy, False otherwise.
        
    '''
    with os.scandir(path) as scan:
        return next(scan, None) is None

def to_image(video_path, output_path, frame_skip, force_flag):
    '''Converts mp4 video into individual frames and stores in 
    provided output path.

    Parameters:
        video_path(str): Path to video.
        output_path(str): Path to output dir.
    '''
    input_abs_path = str(video_path.resolve())
    output_abs_path = str(output_path.resolve())
    if not str(input_abs_path).endswith(".mp4"):
        raise ValueError(f"Input is not an mp4 file.")

    if os.path.exists(output_abs_path):
        if not is_dir_empty(output_abs_path):
            if not force_flag:
                raise IOError(f"Files already exist in {output_abs_path}.")
            else:
                for filename in os.listdir(output_abs_path):
                    file_path = os.path.join(output_abs_path, filename)
                    if filename[-4:].lower() == ".jpg":
                        os.unlink(file_path)
    else:
        raise FileNotFoundError(f"{output_abs_path} does not exist.")

    vid = cv2.VideoCapture(str(input_abs_path))

    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver)  < 3 :
        fps = vid.get(cv2.cv.CV_CAP_PROP_FPS)
    else :
        fps = vid.get(cv2.CAP_PROP_FPS)
    frame_delta_t = frame_skip/fps #how far apart the frames are

    count = 0
    result_average = None
    while True:
        try:
            read_success, image = vid.read()
            if result_average is None:
                result_average = image.copy()
            else:
                if image is not None:
                    result_average = result_average * (count / (count+1)) \
                                     + image * (1 / (count+1))

            if not read_success:
                if count <= 0:
                    raise ExtractFrameException(f"""Unable to read any frames \
                                                from {input_abs_path}.""")
                break #TODO: how do we detect error in vid.read()
            print('Read a new frame: ', read_success, file=sys.stderr)
            if count%frame_skip == 0:
                write_path = f"{output_abs_path}{os.sep}{str(count).zfill(5)}.jpg"
                write_success = cv2.imwrite(write_path, image) # save as JPEG
            if not write_success:
                raise ExtractFrameException(f"Unable to save to jpg.")
        except Exception as e:
            raise ExtractFrameException(f"""Exception converting image \
                                        jpg format. {e}""")
        count += 1
    cv2.imwrite(f"{output_abs_path}{os.sep}average.jpg", result_average)
    return fps, frame_delta_t

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
        usage="%(prog)s [-h] [-v] -i INPUT_PATH -o OUTPUT_PATH -s SKIP_NUM [-f]", 
        add_help=False,
    description="Converts mp4 video into photo"
    )

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--infile", action="store", type=pathlib.Path, 
                          required=True, help = "Full path to an mp4 file")
    required.add_argument("-o", "--outdir", action="store", type=pathlib.Path, 
                          required=True, help = """Empty directory to store frames in. \
                          Output = nnnn.jpg and starts from 0000 onwards""")
    required.add_argument("-s", "--skip", action="store", default="1", type=int, 
                          required=True, help = "Choose interval of frames to process.")

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
        fps, frame_delta_t = to_image(args.infile, args.outdir, args.skip, 
                                      args.force)
        print(f"Skip frames: {args.skip}")
        print(f"frame_rate = {fps}")
        print(f"frame_delta_t = {frame_delta_t}")
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()