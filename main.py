import cv2
import os
import argparse

IF_SHOW = 0

def getCropImage(img, r, fileName):

    img = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    saveFig(img, fileName, "croped")

    if IF_SHOW:
        cv2.imshow("croped", img)

def getBoxedImage(img, r, fileName):

    # represents the top left corner of rectangle
    start_point = (r[0], r[1])
    # represents the bottom right corner of rectangle
    end_point = (r[0]+r[2], r[1]+r[3])
    # Blue color in BGR
    color = (0, 0, 255)
    # Line thickness of 2 px
    thickness = 5

    cv2.rectangle(img, start_point, end_point, color, thickness)
    saveFig(img, fileName, "boxed")

    if IF_SHOW:
        cv2.imshow("boxed", img)

OUTPUT_FOLDER = "output"
if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

def saveFig(img, fileName, funcName):

    _fileName = os.path.splitext(fileName)[0]
    cv2.imwrite(f"{OUTPUT_FOLDER}/{_fileName}_{funcName}.jpg", img)

if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder")
    args = parser.parse_args()

    img_paths = os.listdir(args.input_folder)

    if_first = 1
    if_resize = 0

    for file_name in img_paths:

        img = cv2.imread(os.path.join(args.input_folder, file_name))
        if if_resize:
            img = cv2.resize(img, (1024, 1024))
        
        if if_first:
            if_first = 0
            r = cv2.selectROI(img)

        # r is represent as :
        # (31, 65, 125, 120)
        #  ^   ^    ^    ^
        #  |   |    |    |
        #  x1  y1   |    y2 = 120 + 65
        #          x2 = 125 + 31

        getCropImage(img, r, file_name)
        getBoxedImage(img, r, file_name)

    if IF_SHOW:
        cv2.waitKey(0)