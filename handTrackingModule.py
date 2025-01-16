import numpy as np
import os
import mediapipe as mp
import handTrackingModule as htm
import time
import cv2 as cv
import math

# Initialize webcam
img = cv.VideoCapture(0)
img.set(cv.CAP_PROP_FRAME_WIDTH, 1080)
img.set(4, 720)

# Load background image
a1 = cv.imread("main.jpg")
y, x, c = a1.shape

# Initialize the hand tracking module
obj = htm.HandTracker()

# Canvas for drawing
imgCanvas = np.zeros((720, 1280, 3), dtype="uint8")
imgThickness = 5

# Initialize position for drawing
xp, yp = 0, 0

# Initialize color and eraser-mode status
colorIndex = 0
eraser_mode = False

while True:
    _, frame = img.read()
    frame = cv.flip(frame, 1)

    # Detect hand gestures
    frame = obj.findHands(frame, draw=False)
    lmlist = obj.handsPosition(frame, draw=False)

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingersUP = obj.fingerUp(frame)

        if fingersUP[1] and fingersUP[2]:  # Red color
            colorIndex = 0

        elif fingersUP[1] and not fingersUP[2] and fingersUP[0]:  # Green color
            colorIndex = 1

        elif fingersUP[1] and not fingersUP[2] and not fingersUP[0]:  # Blue color
            colorIndex = 2

        elif fingersUP[4] and fingersUP[0] and fingersUP[1]:  # Eraser
            eraser_mode = True

        if eraser_mode:  # Erase
            color = (255, 255, 255)  # White color to erase
            cv.line(imgCanvas, (xp, yp), (x1, y1), color, imgThickness)

        elif colorIndex < 3:  # Draw
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if colorIndex == 0:
                color = (0, 0, 255)  # Red color
            elif colorIndex == 1:
                color = (0, 255, 0)  # Green color
            elif colorIndex == 2:
                color = (255, 0, 0)  # Blue color

            cv.line(imgCanvas, (xp, yp), (x1, y1), color, imgThickness)
            cv.line(frame, (xp, yp), (x1, y1), color, imgThickness)

            xp, yp = x1, y1

    # Place background image on top of the frame
    frame[0:y, 0:x] = a1

    cv.imshow("video", frame)
    cv.imshow("imgCanvas", imgCanvas)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()
