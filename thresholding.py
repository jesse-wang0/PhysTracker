import sys, os
import pathlib
import cv2
from PIL import Image

ball_info = []
background_info = []

img1 = cv2.imread("C:\\Users\\jesse\\git_projects\\example2\\frames\\00002.jpg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
x1 = 180
x2 = 230
y1 = 90
y2 = 140

for i, row in enumerate(img1):
    for j, pixel in enumerate(row):
        if x1 < i < x2 and y1 < j < y2:
            ball_info.append(pixel)

print(min(ball_info))
print(max(ball_info))
mean_ball = sum(ball_info) / len(ball_info)
print(mean_ball)

back_x1 = 400
back_x2 = 600
back_y1 = 200
back_y2 = 400

for i, row in enumerate(img1):
    for j, pixel in enumerate(row):
        if back_x1 < i < back_x2 and back_y1 < j < back_y2:
            background_info.append(pixel)

print(min(background_info))
print(max(background_info))
mean_background = sum(background_info) / len(background_info)
print(mean_background)

print(f"Difference:  {abs(mean_background - mean_ball)}")

cv2.rectangle(img1,(x1,y1),(x2,y2),(0,255,0),3)
cv2.rectangle(img1,(back_x1,back_y1),(back_x2,back_y2),(0,255,0),3)

cv2.imshow('Foo',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()