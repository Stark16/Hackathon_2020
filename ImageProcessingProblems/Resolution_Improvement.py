import cv2
import numpy as np
import glob, os

A4_width=8.27 #inch
A4_height=11.69 #inch
DPI=300
required_width=int(A4_width*DPI)
required_height=int(A4_height*DPI)

source_path='./images/LowResolution/'
destination_path='./images/LowResolution/LowResultion_improved/'

for pathAndFilename in glob.iglob(os.path.join(source_path,"*.jpg")):
    #Taking the path data and opening the images
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(title+ext)
    img = cv2.imread(source_path+title+ext,0)

    dimension = img.shape
    if dimension[1]>dimension[0]:
        # its a potrait image
        scaling_factor = int(100 * required_height / dimension[1])
    else:
        #its a landscape image
        scaling_factor = int(100 * required_width / dimension[0])

    # scaling_factor=100
    width = int(dimension[1] * scaling_factor / 100)
    height = int(dimension[0] * scaling_factor / 100)
    resize_img_size = (width, height)
    img = cv2.resize(img, resize_img_size)
    #cv2.imshow("Resized image",img)

    # Defining filter parameter
    kernal = np.ones((2, 2), np.uint8)

    # Performing bilaternal filtering to remove paper-salt noise and intact color space
    # This will remove black noise from white background
    bilateral = cv2.bilateralFilter(img, 30, 30, 75)

    # Taking negative image to remove white noise from black background

    # UNCOMMENT THIS LINE IF YOU WANT TO REMOVE WATERMARK ALSO (ALSO CHANGE BILATERAL VAR TO BW_IMG IN NEXT LINE) ret, bw_img = cv2.threshold(bilateral, 180, 255, cv2.THRESH_BINARY)
    neg = cv2.bitwise_not(bilateral)

    # REMOVE WHITE NOISE
    opening = cv2.morphologyEx(neg, cv2.MORPH_OPEN, kernal)
    # OPENINIG WILL MAKE SOME PART OF TEXT MISSING TO RESTORE IT DO CLOSING
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernal)

    # CONVERT IMAGE INTO ORIGINAL COLOR_SPACE
    denonised_img = cv2.bitwise_not(closing)

    # SAVE DENOISED IMAG INTO FOLDER NAMED "Noise_removed"
    Filename = destination_path + title + ext
    cv2.imwrite(Filename, denonised_img)

print("Done")