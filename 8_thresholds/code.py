import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read(0)

    # Перевод изображения в Ч/Б
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Разные методы нахождения порогов
    ret, t1 = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    ret, t2 = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)
    ret, t3 = cv2.threshold(frame, 127, 255, cv2.THRESH_TRUNC)
    ret, t4 = cv2.threshold(frame, 127, 255, cv2.THRESH_TOZERO)
    ret, t5 = cv2.threshold(frame, 127, 255, cv2.THRESH_TOZERO_INV)

    cv2.imshow('t1', t1)
    cv2.imshow('t2', t2)
    cv2.imshow('t3', t3)
    cv2.imshow('t4', t4)
    cv2.imshow('t5', t5)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()