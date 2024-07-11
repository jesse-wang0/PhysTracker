rem Example Workflow
py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\empty_frames" -f
py thresholding.py -p1 "..\example2\frames\00002.jpg" -p2 "..\example2\frames\00004.jpg" -x (180,230) -y (90,140)
py combine_images.py -i "..\example2\empty_frames" -o "..\example2\frames" -t 15
py blob_detection.py -i "..\example2\empty_frames\mask\mask.png" -o "..\example2\empty_frames\mask" -r (164,57,1023,663)
py get_positions.py -i "..\example2\testing_frames" -d 0.041666666666666664 -r (164,57,1023,663) -m 0.02
py generate_graph.py -i "..\example2\empty_frames\data\position_data.csv" -t "y_acceleration"

rem Testing for extract_frame CLI
py extract_frame.py -i "..\example2\video\fake.mp4" -o "..\example2\empty_frames" rem Invalid input file
py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\zxczxczx" rem Invalid output path
py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\frames" rem Normal use of the cli
py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\nonempty_frames" -f rem Check if force works when output dir is not empty