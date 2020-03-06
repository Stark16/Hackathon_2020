import cv2
import numpy as np
from matplotlib import pyplot as plt

im_name = cv2.imread("./Data/filled_sample.jpg")
og_image = im_name.copy()
og_dim = (og_image.shape[0], og_image.shape[1])
new_dim = (int(og_dim[0]/3), int(og_dim[1]/3))

#im_name = cv2.resize(im_name, new_dim)
print(im_name.shape[0], new_dim[0], og_dim)

gray = cv2.cvtColor(im_name, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edge = cv2.Canny(gray, 100, 500, apertureSize=3)
plt.imshow(edge)
plt.show()
# cv2.waitKey(0)
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
        #print("Horizontal")

        if x1 < x2:
            #print("Bottom line")
            left_bottom = (int(x1*3), int(y1*3))
            right_bottom = (int(x2*3), int(y2*3))
        elif x1 > x2:
            #print("Top Line")
            right_top = (int(x1*3), int(y1*3))
            left_top = (int(x2*3), int(y2*3))

print(left_top, right_bottom)

# Performing Geometrical transform:

pt1 = np.float32([[left_top], [right_top], [left_bottom], [right_bottom]])
pt2 = np.float32([[0, 0], [og_image.shape[0], 0], [0, og_image.shape[1]], [og_image.shape[0], og_image.shape[1]]])

matrix = cv2.getPerspectiveTransform(pt1, pt2)
new_image = cv2.warpPerspective(og_image, matrix, (og_image.shape[1], og_image.shape[0]))

# Corners are printed clockwise starting from left top and are colour coded as Blue, Green, Red and black respectively.
cv2.circle(og_image, left_top, 6, (255, 0, 0), 3)
cv2.circle(og_image, right_top, 6, (0, 255, 0), 3)
cv2.circle(og_image, right_bottom, 6, (0, 0, 255), 3)
cv2.circle(og_image, left_bottom, 6, (0, 0, 0,), 3)

plt.subplot(121),plt.imshow(og_image)
plt.subplot(122), plt.imshow(new_image)
plt.show()

# cv2.imshow("pic", im_name)
# cv2.imshow("new", new_image)
# cv2.imshow("page", page)
# cv2.imshow("edge", edge)
# cv2.waitKey(0)