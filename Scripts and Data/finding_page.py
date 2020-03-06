import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

im = cv2.imread("./Data/blank_simple (1).jpg",0)
copy = im.copy()

im = cv2.resize(im, (int (im.shape[0]/5), int(im.shape[1]/5) ) )
point = (354, 46)
cv2.circle(im, point, 6, (0, 255, 0), -1)
point = (354*5, 46*5)
cv2.circle(copy, point, 6, (0, 255, 0), -1)

plt.subplot(121), plt.show(im)
plt.subplot(122), plt.show(copy)