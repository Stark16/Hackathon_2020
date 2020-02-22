import cv2
import numpy as np

im = cv2.imread("./Data/blank_4.jpg")
im_name = cv2.resize(im, (600,700))
gray = cv2.cvtColor(im_name, cv2.COLOR_BGR2GRAY)

edge = cv2.Canny(gray, 100, 500, apertureSize=3)
cv2.imshow("Adaptive", edge)
cv2.waitKey(0)

item,  hierchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for con in item:
    area_cont = cv2.contourArea(con)
    if area_cont > 1000:
        cv2.drawContours(im_name, con, -1, (0,255,0), 3)


cv2.imshow("cont", im_name)
cv2.waitKey(0)
