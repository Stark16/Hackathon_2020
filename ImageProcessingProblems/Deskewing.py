import cv2
import numpy as np
import glob, os

source_path='./images/Skew/'
destination_path='./images/Skew/deskewd_images/'

for pathAndFilename in glob.iglob(os.path.join(source_path,"*.jpg")):
    #Taking the path data and opening the images
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(title+ext)
    img = cv2.imread(source_path+title+ext,0)
    dimension=img.shape

    # adding boarder line of 10% just to make sure anchor point lies properly within image
    border_size = int(0.1*max(img.shape))
    img = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, 1)

    # converting image to negtive i.e. content is kept white and bg is black
    binary=cv2.bitwise_not(img)

    coordinates = np.column_stack(np.where(binary > 100))

    # Cv2.minArea Rect creates rectangle around the given c0-ordinates and also calculates the angle at which the major axis of image lies
    ang = cv2.minAreaRect(coordinates)[-1]

    if ang < -45:
        ang = -(90 + ang)
    else:
        ang = -ang
    height, width = img.shape[:2]
    center_img = (width / 2, height / 2)

    # image is rotated by given angle.
    rotationMatrix = cv2.getRotationMatrix2D(center_img, ang, 1.0)
    rotated_img = cv2.warpAffine(binary, rotationMatrix, (width, height), 0)

    # converting to original image. Content is black on white background
    gray_img = cv2.bitwise_not(rotated_img)

    # Saving the file
    Filename = destination_path + title + ext
    cv2.imwrite(Filename, gray_img)
print("Done")