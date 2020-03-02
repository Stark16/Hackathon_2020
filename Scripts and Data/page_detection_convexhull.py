import cv2
import numpy as np

im_name = cv2.imread("./Data/blank_simple (2).jpg")
im_name = cv2.resize(im_name, (700, 700), interpolation=True)
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

page = np.empty_like(gray)
page[:, :] = 0

cv2.drawContours(page, item, max_index[0], (255, 255, 255), 1)

corners = cv2.goodFeaturesToTrack(page, 4, 0.01, 60)
hull = cv2.convexHull(corners, clockwise=True)

lines = []
for i in range(4):
    x1, y1 = hull[i].ravel()
    if i == 3:
        x2, y2 = hull[0].ravel()
    else:
        x2, y2 = hull[i+1].ravel()
    lines.append([(x1, y1),  (x2, y2)])
    cv2.line(im_name, (x1, y1), (x2, y2), (255, 255, 0), 3)

cv2.imshow("pic", im_name)
cv2.waitKey(0)
