import cv2
import numpy as np

im = cv2.imread("./Data/blank_simple (4).jpg")
im_name= cv2.resize(im, (1000, 700))
gray = cv2.cvtColor(im_name, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray, 100, 200, apertureSize=3)

item, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

area_cont = np.arange( len(item) )
i = 0
for cont in item:
    area_cont[i] = cv2.contourArea(cont)
    i += 1
max_area = area_cont.max()
max_index = np.where(area_cont == max_area)

cv2.drawContours(im_name, item, max_index[0], (0, 255, 0), 3)

'''cv2.imshow("Contour", im_name)
cv2.imshow("edge", edge)
cv2.waitKey(0)
'''

blank = np.empty_like(gray)
cv2.drawContours(blank, item, max_index[0], (255, 255, 255), 3)
blank = np.float32(blank)

dst = cv2.cornerHarris(blank, 2, 3, 0.04)


cv2.imshow("Boundary", blank)
cv2.waitKey(0)