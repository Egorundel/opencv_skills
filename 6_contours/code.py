import cv2
import numpy as np

# считываение видеопотока с веб-камеры
cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')

while True:
    ret, frame = cap.read()

    # перевод изображения в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # определение краёв
    edge = cv2.Canny(gray, 100, 200)

    # определение контуров
    contours, h = cv2.findContours(edge, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # рисование контуров
    cv2.drawContours(frame, [contours[0]], -1, (0,0,255), 5)

    cv2.imshow('frame', frame)
    cv2.imshow('edge', edge)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

print(contours)
print(h)