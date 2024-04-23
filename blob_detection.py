import cv2
import numpy as np


img = cv2.imread("final.png", cv2.IMREAD_GRAYSCALE)
# Create SimpleBlobDetector object with default parameters
params = cv2.SimpleBlobDetector_Params()

# Set up the detector parameters
params.filterByColor = 1
params.blobColor = 255
params.filterByArea = True
params.minArea = 100

params.filterByCircularity = False

params.filterByConvexity = True
params.minConvexity = 0.2

params.filterByInertia = True
params.minInertiaRatio = 0.01
"""
params.filterByArea = True
params.minArea = 100

params.filterByCircularity = False

params.filterByConvexity = True
params.minConvexity = 0.90

params.filterByInertia = True
params.minInertiaRatio = 0.001
"""
# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs using the detector
keypoints = detector.detect(img)

# Draw detected blobs as red circles
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Display the image with the detected blobs
cv2.imshow('Blob Detection', img_with_keypoints)

# Wait for a key press and then exit
cv2.waitKey(0)
cv2.destroyAllWindows()