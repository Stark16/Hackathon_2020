import cv2
import numpy as np


im = cv2.imread("./Data/blank_simple (3).jpg")
im_name = cv2.resize(im, (700, 700))
gray = cv2.cvtColor(im_name, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray, 100, 200, apertureSize=3)

item,  hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


area_cont = np.arange(len(item))
i = 0
for con in item:
    area_cont[i] = cv2.contourArea(con)
    i += 1

max_area = np.amax(area_cont)
max_index = np.where(area_cont == max_area)
print(max_area)


cv2.drawContours(im_name, item, max_index[0] , (0,255,0), 3)

cv2.imshow("cont", im_name)
cv2.waitKey(0)
