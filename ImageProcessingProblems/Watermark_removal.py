import glob, os
import cv2
import numpy as np

source_path='./images/Watermark/'
destination_path='./images/Watermark/cleaned_images/'

for pathAndFilename in glob.iglob(os.path.join(source_path,"*.jpg")):
    #print(pathAndFilename)
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(title+ext)
    # reading the img file
    img = cv2.imread(source_path+title+ext,1)

    # applying histogram elimination technique
    alpha = 2.0
    beta = -100
    clean_img = alpha * img + beta
    clean_img = np.clip(clean_img, 0, 255).astype(np.uint8)

    # Writing the image file
    Filename=destination_path+title+ext
    cv2.imwrite(Filename,clean_img)

print("done")
