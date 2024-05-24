import sys, os
import pathlib
import cv2
from PIL import Image
import argparse

img1 = cv2.imread("C:\\Users\\jesse\\git_projects\\example2\\frames\\00002.jpg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread("C:\\Users\\jesse\\git_projects\\example2\\frames\\00004.jpg")
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

x1 = 180
x2 = 230
y1 = 90
y2 = 140

x1 = 500
x2 = 700
y1 = 200
y2 = 400


differences = []

for xi in range(x1, x2):
    for yi in range(y1, y2):
        first_frame_area = int(img1[yi][xi])
        second_frame_area = int(img2[yi][xi])
        diff = abs(first_frame_area-second_frame_area)
        differences.append(diff)

threshold = sum(differences)/len(differences)

cv2.rectangle(img1,(x1,y1),(x2,y2),(0,255,0),3)
cv2.imshow('Foo',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()