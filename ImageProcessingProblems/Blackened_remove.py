import glob, os
import cv2
import numpy as np

source_path='./images/Blackened/'
destination_path='./images/Blackened/Blackend_removed/'
kernel = np.ones((20,20),np.uint8)
for pathAndFilename in glob.iglob(os.path.join(source_path,"*.jpg")):
    #Taking the path data and reading the image
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(title+ext)
    img_original = cv2.imread(source_path+title+ext,0)
    # Converting image to black and white (BINARY IMAGE)
    ret, bw_img = cv2.threshold(img_original, 127, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_not(bw_img)
    # Errosion
    erroded_img = cv2.cv2.erode(img, kernel, iterations=1)
    # Dilation
    dilated_img = cv2.cv2.dilate(erroded_img, kernel, iterations=1)
    height, width = dilated_img.shape
    # Checking for big black region and converting it into white
    for i in range(height):
        for j in range(width):
            if (dilated_img[i][j] != 0):
                img_original[i][j] = 255
    # Saving the new file
    Filename=destination_path+title+ext
    cv2.imwrite(Filename,img_original)
    # cv2.waitKey(0)

print("done")