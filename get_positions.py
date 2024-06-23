import cv2, os
import numpy as np
from blob_detection import setup_detector

input_abs_path = "C:\\Users\\jesse\\git_projects\\example2\\testing_frames"
average_background_path = "C:\\Users\\jesse\\git_projects\\example2\\testing_frames\\average.jpg"
average_background = cv2.imread(average_background_path)
img_files = os.listdir(input_abs_path)
fps = 24.0
frame_duration = 0.041666666666666664

x_list = []
y_list = []

for i in img_files:
    img = cv2.imread(f"{input_abs_path}/{i}")
    difference = cv2.absdiff(img, average_background)
    difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    f_, thresholded_diff = cv2.threshold(difference, 15, 255, cv2.THRESH_BINARY)

    detector = setup_detector(min_area=200, max_area=2000, circularity=0.3, 
                                convexity=0.1, inertia=0.01)
    keypoints = detector.detect(thresholded_diff)

    colour = (0,0,255)
    flag_match = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    img_with_keypoints = cv2.drawKeypoints(difference, keypoints, np.array([]), 
                                            colour, flag_match)
    
    max_area = 0
    max_area_point = None
    for key_point in keypoints:
        x = key_point.pt[0]
        y = key_point.pt[1]
        s = key_point.size
        if 164 < x < 1187 and 57 < y < 720:
            if s > max_area:
                max_area_point = key_point
    if max_area_point is not None:
        x_list.append(max_area_point.pt[0])
        y_list.append(max_area_point.pt[1])


#position -x
#position - y
#velocity - x
#velocity -y
#acceleration - x
#acceleration - y