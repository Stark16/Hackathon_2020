import cv2
import numpy as np
from matplotlib import  pyplot as plt

im_name = cv2.imread("./Data/noisy_bill 1.jpg")
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
# print(corners)
hull = cv2.convexHull(corners, clockwise=True)

for i in range(4):
    x1, y1 = hull[i].ravel()

    if i == 3:
        x2, y2 = hull[0].ravel()
    else:
        x2, y2 = hull[i+1].ravel()

    x_slope = abs(x2 - x1)
    y_slope = abs(y2 - y1)

    if x_slope > y_slope:
        print("Horizontal")

        if x1 < x2:
            print("Bottom line")
            left_bottom = (x1, y1)
            right_bottom = (x2, y2)
        elif x1 > x2:
            print("Top Line")
            right_top = (x1, y1)
            left_top = (x2, y2)

    elif y_slope > x_slope:
        print("Vertical")

        if y1 < y2:
            print("Left line")
        elif y1 > y2:
            print("Right line")


# Performing affine transform:

pt1 = np.float32([[left_top], [right_top], [left_bottom]])
pt2 = np.float32([[0, 0], [700, 0], [0, 700]])

matrix = cv2.getAffineTransform(pt1, pt2)
new_image = cv2.warpAffine(im_name, matrix, (700, 700))

# Corners are printed clockwise starting from left top and are colour coded as Blue, Green, Red and black respectively.
cv2.circle(im_name, left_top, 6, (255, 0, 0), 3)
cv2.circle(im_name, right_top, 6, (0, 255, 0), 3)
cv2.circle(im_name, right_bottom, 6, (0, 0, 255), 3)
cv2.circle(im_name, left_bottom, 6, (0, 0, 0,), 3)

plt.subplot(121),plt.imshow(im_name)
plt.subplot(122), plt.imshow(new_image)
plt.show()
# cv2.imshow("pic", im_name)
# cv2.imshow("new", new_image)
# cv2.imshow("page", page)
# cv2.imshow("edge", edge)
# cv2.waitKey(0)
