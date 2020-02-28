import cv2
import numpy as np
import glob, os


source_path='./images/Noise/'
destination_path='./images/Noise/Noise_removed/'

for pathAndFilename in glob.iglob(os.path.join(source_path,"*.jpg")):
    #Taking the path data and opening the images
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(title+ext)
    img = cv2.imread(source_path+title+ext,0)

    #Resizing image
    dimension = img.shape
    scaling_factor = int(100 * 4000 / dimension[0])
    width = int(dimension[1] * scaling_factor / 100)
    height = int(dimension[0] * scaling_factor / 100)
    resize_img_size = (width, height)
    img = cv2.resize(img, resize_img_size)

    # Defining filter parameter
    kernal = np.ones((2, 2), np.uint8)

    #Performing bilaternal filtering to remove paper-salt noise and intact color space
    # This will remove black noise from white background
    bilateral=cv2.bilateralFilter(img, 30, 30, 75)

    #Taking negative image to remove white noise from black background

    #UNCOMMENT THIS LINE IF YOU WANT TO REMOVE WATERMARK ALSO (ALSO CHANGE BILATERAL VAR TO BW_IMG IN NEXT LINE) ret, bw_img = cv2.threshold(bilateral, 180, 255, cv2.THRESH_BINARY)
    neg = cv2.bitwise_not(bilateral)

    # REMOVE WHITE NOISE
    opening = cv2.morphologyEx(neg, cv2.MORPH_OPEN, kernal)
    # OPENINIG WILL MAKE SOME PART OF TEXT MISSING TO RESTORE IT DO CLOSING
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernal)

    # CONVERT IMAGE INTO ORIGINAL COLOR_SPACE
    denonised_img=cv2.bitwise_not(closing)

    # SAVE DENOISED IMAG INTO FOLDER NAMED "Noise_removed"
    Filename = destination_path + title + ext
    cv2.imwrite(Filename, denonised_img)

print("Done")