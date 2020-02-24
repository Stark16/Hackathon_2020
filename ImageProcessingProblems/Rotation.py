import cv2
import imutils
source_path='images/Rotation/'
destination_path='images/Rotation/Rotated_images/'

img_source=['rotate-1.jpg','rotate-2.jpg','rotate-3.jpg','rotate-4-brokenlines.jpg','rotate-5-brokenlines.jpg']

rotation_matrix=[180,-90,90,180,-90]

if len(img_source)==len(rotation_matrix):
     # TAKING IMG AND ROTATING IT ACCORDINGLY ROTATION MATRIX

     # Checking if rotation matrix have equal rotation values as that of file name
    for i in range(len(img_source)):
        filename=img_source[i]
        img_path = source_path+filename

        # Reading original image
        img = cv2.imread(img_path, 1)
        #cv2.imshow("Original image", img)

        angle=rotation_matrix[i]

        #Rotating image with imutils
        rotated_img = imutils.rotate_bound(img, angle)
        #cv2.imshow("Rotated image", rotated_img)

        cv2.imwrite(destination_path+filename,rotated_img)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    print("THE SIZE OF IMAGES AND ROTATION MATRIX DOES NOT MATCH")

print("Done...")
