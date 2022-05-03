import numpy as np
import cv2 as cv
cap = cv.VideoCapture('/Users/jackboynton/Library/Application Support/Dolphin/Dump/Frames/RMCP01_2022-05-01_15-51-17_0.avi')
while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()