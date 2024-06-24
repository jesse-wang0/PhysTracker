

py extract_frame.py -i "..\example2\video\fake.mp4" -o "..\example2\empty_frames"

py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\frames"
py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\nonempty_frames" -f

py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\zxczxczx"




py extract_frame.py -i "..\example2\video\Bouncing ball reference.mp4" -o "..\example2\testing_frames"
py thresholding.py -i "..\example2\frames\00002.jpg" -j "..\example2\frames\00004.jpg" -x "(180,90)" -y "(230,140)"
py combine_images.py -i "..\example2\frames" -o "..\example2\empty_frames" -t 15
py blob_detection.py -i "..\example2\empty_frames\final.png"
py get_positions.py -i "..\example2\testing_frames" -a "..\example2\testing_frames\average.jpg" -d 0.041666666666666664 -r (164,1187,57,720) -m 0.02
py generate_graph.py -i "position_data.csv" -t "y_acceleration"