import numpy as np
import os
import mediapipe as mp
import handTrackingModule as htm
import time
import cv2 as cv
import math

img = cv.VideoCapture(0)
img.set(cv.CAP_PROP_FRAME_WIDTH, 1080)
img.set(4, 720)
print(img.get(3))

imgCanvas = np.zeros((720, 1280, 3), dtype="uint8")

a1 = cv.imread("main.jpeg")

imgThickness = 5

y, x, c= a1.shape
print(y)
color = (255, 0, 0)

obj = htm.handTracking()

xp, yp = 0, 0

while True:
    _, frame = img.read()
    frame = cv.flip(frame, 1)
    obj.findHands(frame, draw=False)
    lmlist = obj.handsPosition(frame, draw=False)

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingersUP = obj.fingerUp(frame)

        #selection mode
        if fingersUP[1] and fingersUP[2]:
            cv.rectangle(frame, (x1, y1-25), (x2, y2+25), color, -1)
            xp, yp = 0, 0

            if y1 < 248:
                if x1 < 198 and x1 > 0:
                    color = (0, 0, 255)
                    imgThickness = 5
                    print("red")

                elif x1 < 432 and x1 > 198:
                    color = (0, 255, 0)
                    imgThickness = 5
                    print("green")

                elif x1 < 855 and x1 > 640:
                    color = (255, 0, 0)
                    imgThickness = 5
                    print("blue")

                elif x1 < 1076 and x1 > 856:
                    color = (0, 0, 0)
                    imgThickness = 40

        #draw mode
        if fingersUP[1] and fingersUP[2] == False:
            cv.circle(frame, (x1, y1), 12, color, -1)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv.line(frame, (xp,yp), (x1, y1), color, imgThickness)
            cv.line(imgCanvas, (xp,yp), (x1, y1), color, imgThickness)
            xp, yp = x1, y1

    frame[0:y, 0:x] = a1

    cv.imshow("video", frame)
    cv.imshow("imgCanvas", imgCanvas)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()