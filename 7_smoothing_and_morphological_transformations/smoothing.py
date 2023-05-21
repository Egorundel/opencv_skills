import cv2
import numpy as np

# считываение видеопотока с веб-камеры
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    # размытие (averaging)
    blur = cv2.blur(frame, (3,3))
    cv2.imshow('blur', blur)

    # размытие Гаусса
    gblur = cv2.GaussianBlur(frame, (5,5), 0)
    cv2.imshow('Gaussian Blur', gblur)

    # билатеральное размытие
    bblur = cv2.bilateralFilter(frame, 9, 75, 75)
    cv2.imshow('Bilateral Filter', bblur)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()