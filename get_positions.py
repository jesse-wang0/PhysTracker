import cv2, os, math
import numpy as np
from blob_detection import setup_detector
import matplotlib.pyplot as plt

input_abs_path = "C:\\Users\\jesse\\git_projects\\example2\\testing_frames"
average_background_path = "C:\\Users\\jesse\\git_projects\\example2\\testing_frames\\average.jpg"
average_background = cv2.imread(average_background_path)
img_files = os.listdir(input_abs_path)
fps = 24.0
frame_duration = 0.041666666666666664

x_list = []
y_list = []
image_height = average_background.shape[0]

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
        y_list.append(image_height - max_area_point.pt[1])

#position -x
def plot_x():
    x_coord = np.array(x_list)
    time = np.zeros(len(x_list))
    for i in range(len(x_list)):
        time[i] = frame_duration * i
    plt.plot(time, x_coord, 'o')
    plt.xlabel('Time (seconds)')
    plt.ylabel('X Coordinate')
    plt.title('X Coordinate vs Time')

#position - y
def plot_y():
    y_coord = np.array(y_list)
    time = np.zeros(len(y_list))
    for i in range(len(y_list)):
        time[i] = frame_duration * i
    plt.plot(time, y_coord, 'o')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Y Coordinate')
    plt.title('Y Coordinate vs Time')

#velocity - x
def plot_x_velocity():
    x_velocity = np.zeros(len(x_list) - 1)
    for i in range(len(x_list) - 1):
        velocity = (x_list[i+1] - x_list[i]) / frame_duration 
        x_velocity[i] = velocity
    time = np.zeros(len(x_list) - 1)
    for i in range(1, len(x_list)):
        time[i-1] = frame_duration * i
    plt.plot(time, x_velocity, 'o')
    plt.xlabel('Time (seconds)')
    plt.ylabel('X Velocity')
    plt.title('X Velocity vs Time')

#velocity -y
def plot_y_velocity():
    y_velocity = np.zeros(len(y_list) - 1)
    for i in range(len(y_list) - 1):
        velocity = (y_list[i+1] - y_list[i]) / frame_duration 
        y_velocity[i] = velocity
    time = np.zeros(len(y_list) - 1)
    for i in range(1, len(y_list)):
        time[i-1] = frame_duration * i
    plt.plot(time, y_velocity, 'o')
    plt.xlabel('Time (seconds)')
    plt.ylabel('X Velocity')
    plt.title('X Velocity vs Time')

#acceleration - x

#acceleration - y

plot_y_velocity()
plt.grid(True)
plt.show()