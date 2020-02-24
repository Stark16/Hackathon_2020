import cv2
import numpy as np
import glob, os


source_path='./images/Perspective/'
destination_path='./images/Perspective/Perspective_removed/'

for pathAndFilename in glob.iglob(os.path.join(source_path,"*.jpg")):
    #Taking the path data and opening the images
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(title+ext)
    img = cv2.imread(source_path+title+ext,0)
    dimension = img.shape
    # print(img.shape)
    border_size = int(0.1 * max(img.shape))
    img = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, 1)
    dimension = img.shape
    scaling_factor = int(100 * 900 / dimension[0])
    #scaling_factor=100
    width = int(dimension[1] * scaling_factor / 100)
    height = int(dimension[0] * scaling_factor / 100)
    resize_img_size = (width, height)
    # print('resize imag is ', dimension, resize_img_size)
    img = cv2.resize(img, resize_img_size)
    ret, thresh = cv2.threshold(img, 150, 255, 1)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img_copy = img.copy()
    img_copy2 = img.copy()

    points = np.row_stack(np.where(thresh > 200))

    cnt_array = np.array([[[points[1][0], points[0][0]]]])
    # print('cnt arry start is ',cnt_array)
    for i in range(len(points[0])):
        # print(point)
        b = np.array([[points[1][i], points[0][i]]])
        # print(b)
        cnt_array = np.concatenate((cnt_array, [b]), axis=0)

    hull = cv2.convexHull(cnt_array, returnPoints=True)

    hull_img = cv2.drawContours(img_copy, [hull], -1, (0, 0, 255), 4)

    prev_pt_x = hull[-1][0][0]
    prev_pt_y = hull[-1][0][1]
    # print("prev point location is =",prev_pt_y,prev_pt_x)
    Right_max_info = [999, [999, 999], [999, 999]]
    Left_max_info = [999, [999, 999], [999, 999]]
    Top_max_info = [999, [999, 999], [999, 999]]
    Bottom_max_info = [999, [999, 999], [999, 999]]

    for pts in hull:
        current_pt_y = pts[0][1]
        current_pt_x = pts[0][0]
        distx = (current_pt_x - prev_pt_x) ** 2
        disty = (current_pt_y - prev_pt_y) ** 2
        # print("dist x=",distx,"dist y=",disty)

        # print("x-current=",current_pt_x, " y-current=",current_pt_y,"prev x=", prev_pt_x, "prev y=", prev_pt_y)

        if current_pt_x == prev_pt_x:
            slope_x = 999
            slope_y = 999
            if current_pt_y == prev_pt_y:
                print('BOTH POINTS ARE SAME ----------')
            dist = (current_pt_y - prev_pt_y) ** 2
            # print('infinite slope-y distance', dist)
            if dist > 100:
                current_pt_x = current_pt_x + 1

        if current_pt_y == prev_pt_y:
            slope_y = 999
            slope_x = 999
            dist = (current_pt_x - prev_pt_x) ** 2
            # print('infinite slope-x distance', dist)
            if dist > 100:
                current_pt_y = current_pt_y + 1

        if ((current_pt_y != prev_pt_y) & (current_pt_x != prev_pt_x)):
            # if (True):
            slope_x = (current_pt_y - prev_pt_y) / (current_pt_x - prev_pt_x)
            slope_y = (current_pt_x - prev_pt_x) / (current_pt_y - prev_pt_y)
            if abs(slope_x) < abs(slope_y):
                # print("the y slope is ", slope_y)
                if current_pt_x > prev_pt_x:
                    # print("Its horizontal top side")
                    if (abs(Top_max_info[0]) > abs(slope_x)):
                        Top_max_info[0] = abs(slope_x)
                        Top_max_info[1] = (current_pt_x, current_pt_y)
                        Top_max_info[2] = (prev_pt_x, prev_pt_y)
                else:
                    # print("Its horizontal bottom side")
                    if (abs(Bottom_max_info[0]) > abs(slope_x)):
                        Bottom_max_info[0] = abs(slope_x)
                        Bottom_max_info[1] = (current_pt_x, current_pt_y)
                        Bottom_max_info[2] = (prev_pt_x, prev_pt_y)
            else:
                # print("the x slope is ", slope_x)
                if current_pt_y > prev_pt_y:
                    # print("Its vertical right side")
                    if (abs(Right_max_info[0]) > abs(slope_y)):
                        Right_max_info[0] = abs(slope_y)
                        Right_max_info[1] = (current_pt_x, current_pt_y)
                        Right_max_info[2] = (prev_pt_x, prev_pt_y)
                else:
                    # print("Its vertical left side")
                    if (abs(Left_max_info[0]) > abs(slope_y)):
                        Left_max_info[0] = abs(slope_y)
                        Left_max_info[1] = (current_pt_x, current_pt_y)
                        Left_max_info[2] = (prev_pt_x, prev_pt_y)
        # print("the points are=", pts)
        # print("the slope is ",slope_x,slope_y)

        # line = np.array([[prev_pt_x, prev_pt_y], [current_pt_x, current_pt_y]])
        cv2.circle(img, (current_pt_x, current_pt_y), 2, (0, 0, 255), 4)
        cv2.line(img, (prev_pt_x, prev_pt_y), (current_pt_x, current_pt_y), (0, 255, 0), 2)
        #cv2.imshow("Circle points", img)

        prev_pt_x = current_pt_x
        prev_pt_y = current_pt_y
        # print("________________________________")
        # cv2.waitKey(0)
    # cv2.imshow("Circled Image",Circle_img)
    # print(Top_max_info,Bottom_max_info,Right_max_info,Left_max_info)
    img = cv2.line(img, Top_max_info[1], Top_max_info[2], (0, 255, 0), 2)
    img = cv2.line(img, Bottom_max_info[1], Bottom_max_info[2], (0, 255, 0), 2)
    img = cv2.line(img, Right_max_info[1], Right_max_info[2], (0, 255, 0), 2)
    img = cv2.line(img, Left_max_info[1], Left_max_info[2], (0, 255, 0), 2)

    #cv2.imshow("Boarder selected lines", img)
    # print("Top Max Info ", Top_max_info)
    # print("Right Max Info ", Right_max_info)
    # print("Bottom Max Info ", Bottom_max_info)
    # print("Left Max Info ", Left_max_info)

    # TOP -RIGHT POINT  will need line Top and Right
    x11 = Top_max_info[1][0]
    y11 = Top_max_info[1][1]
    x12 = Top_max_info[2][0]
    y12 = Top_max_info[2][1]

    x21 = Right_max_info[1][0]
    y21 = Right_max_info[1][1]
    x22 = Right_max_info[2][0]
    y22 = Right_max_info[2][1]
    m1 = (y11 - y12) / (x11 - x12)
    m2 = (y21 - y22) / (x21 - x22)
    c1 = (y11 - x11 * (m1))
    c2 = (y21 - x21 * (m2))
    x_sol = int((c1 - c2) / (m2 - m1))
    y_sol = int(m1 * x_sol + c1)
    Top_Right_corner_pt = (x_sol, y_sol)

    # BOTTOM -RIGHT POINT  will need line bottom and Right
    x11 = Bottom_max_info[1][0]
    y11 = Bottom_max_info[1][1]
    x12 = Bottom_max_info[2][0]
    y12 = Bottom_max_info[2][1]

    x21 = Right_max_info[1][0]
    y21 = Right_max_info[1][1]
    x22 = Right_max_info[2][0]
    y22 = Right_max_info[2][1]
    m1 = (y11 - y12) / (x11 - x12)
    m2 = (y21 - y22) / (x21 - x22)
    c1 = (y11 - x11 * (m1))
    c2 = (y21 - x21 * (m2))
    x_sol = int((c1 - c2) / (m2 - m1))
    y_sol = int(m1 * x_sol + c1)
    Bottom_Right_corner_pt = (x_sol, y_sol)

    # Bottom -Left POINT  will need line Bottom and Left
    x11 = Bottom_max_info[1][0]
    y11 = Bottom_max_info[1][1]
    x12 = Bottom_max_info[2][0]
    y12 = Bottom_max_info[2][1]

    x21 = Left_max_info[1][0]
    y21 = Left_max_info[1][1]
    x22 = Left_max_info[2][0]
    y22 = Left_max_info[2][1]
    m1 = (y11 - y12) / (x11 - x12)
    m2 = (y21 - y22) / (x21 - x22)
    c1 = (y11 - x11 * (m1))
    c2 = (y21 - x21 * (m2))
    x_sol = int((c1 - c2) / (m2 - m1))
    y_sol = int(m1 * x_sol + c1)
    Bottom_Left_corner_pt = (x_sol, y_sol)

    # Top -Left POINT  will need line Top and Left
    x11 = Top_max_info[1][0]
    y11 = Top_max_info[1][1]
    x12 = Top_max_info[2][0]
    y12 = Top_max_info[2][1]

    x21 = Left_max_info[1][0]
    y21 = Left_max_info[1][1]
    x22 = Left_max_info[2][0]
    y22 = Left_max_info[2][1]
    m1 = (y11 - y12) / (x11 - x12)
    m2 = (y21 - y22) / (x21 - x22)
    c1 = (y11 - x11 * (m1))
    c2 = (y21 - x21 * (m2))
    x_sol = int((c1 - c2) / (m2 - m1))
    y_sol = int(m1 * x_sol + c1)
    Top_Left_corner_pt = (x_sol, y_sol)

    Page_boarder = (Top_Left_corner_pt, Top_Right_corner_pt, Bottom_Right_corner_pt, Bottom_Left_corner_pt)
    print("Page boarder=", Page_boarder)
    # print("Type of page boarder",type(Page_boarder))
    # print(type(contours))

    #########################################
    img = cv2.line(img, Page_boarder[0], Page_boarder[1], (0, 255, 0), 2)
    img = cv2.line(img, Page_boarder[1], Page_boarder[2], (0, 255, 0), 2)
    img = cv2.line(img, Page_boarder[2], Page_boarder[3], (0, 255, 0), 2)
    img = cv2.line(img, Page_boarder[3], Page_boarder[0], (0, 255, 0), 2)
    # cv2.imshow("Circle points",img)
    #cv2.imshow("Boarder points", img)
    # cv2.imshow("Image copy",img_copy2)
    pts1 = np.float32([[Top_Left_corner_pt[0], Top_Left_corner_pt[1]], [Top_Right_corner_pt[0], Top_Right_corner_pt[1]],
                       [Bottom_Left_corner_pt[0], Bottom_Left_corner_pt[1]],
                       [Bottom_Right_corner_pt[0], Bottom_Right_corner_pt[1]]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img_copy2, matrix, (width, height))
    #cv2.imshow("Dewarped image", result)
    Filename = destination_path + title + ext
    cv2.imwrite(Filename, result)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
print("Done")