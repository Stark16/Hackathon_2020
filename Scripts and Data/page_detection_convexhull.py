import cv2
import numpy as np

im_name = cv2.imread("./Data/blank_simple (3).jpg")
im_name = cv2.resize(im_name, (700, 1200), interpolation=True)
gray = cv2.cvtColor(im_name, cv2.COLOR_BGR2GRAY)

edge = cv2.Canny(gray, 100, 500, apertureSize=3)

item, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cont_area = np.arange(len(item))
i = 0

for contour in item:
    cont_area[i] = cv2.contourArea(contour)
    i += 1

max_area = np.amax(cont_area)
max_index = np.where(cont_area == max_area)

hull = cv2.convexHull(item[int(max_index[0])], clockwise=True)
print(hull)

cv2.drawContours(im_name, hull, -1, (255, 255, 0), 3)
cv2.imshow("pic", im_name)
cv2.waitKey(0)
