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

cv2.drawContours(page, item, max_index[0], (255, 255, 255), 1)

corners = cv2.goodFeaturesToTrack(page, 4, 0.01, 60)
print(corners)
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(page, (x, y), 10, (255, 255, 255), -1)


cv2.imshow("pic", page)
cv2.imshow("lines", im_name)
cv2.waitKey(0)
