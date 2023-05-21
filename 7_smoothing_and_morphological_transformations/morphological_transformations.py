import cv2
import numpy as np

def nothing():
    pass

# считываение видеопотока с веб-камеры
cap = cv2.VideoCapture(0)
cv2.namedWindow('track', cv2.WINDOW_NORMAL)

# создание ползунков
cv2.createTrackbar('H', 'track', 0, 180, nothing)
cv2.createTrackbar('S', 'track', 0, 255, nothing)
cv2.createTrackbar('V', 'track', 0, 255, nothing)

cv2.createTrackbar('HL', 'track', 0, 180, nothing)
cv2.createTrackbar('SL', 'track', 0, 255, nothing)
cv2.createTrackbar('VL', 'track', 0, 255, nothing)

kernel = np.ones((5,5), np.uint8)

while True:
    ret, frame = cap.read()

    # переход в пространство HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # использование ползунков для отсеивания нижней и верхней границ цвета в цветовом пространстве HSV
    h = cv2.getTrackbarPos('H', 'track')
    s = cv2.getTrackbarPos('S', 'track')
    v = cv2.getTrackbarPos('V', 'track')

    hl = cv2.getTrackbarPos('HL', 'track')
    sl = cv2.getTrackbarPos('SL', 'track')
    vl = cv2.getTrackbarPos('VL', 'track')

    lower = np.array([hl, sl, vl])
    upper = np.array([h, s, v])

    # билатеральное размытие
    frame = cv2.bilateralFilter(frame, 9, 75, 75)

    # маска по цвету
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    edge = cv2.Canny(mask, 100, 200)

    contours, h = cv2.findContours(edge,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key = cv2.contourArea, reverse=True)

    try:
        cv2.drawContours(frame, [contours[0]], -1, (255, 0, 0), 5)
    except Exception:
        print()

    cv2.imshow('mask', mask)

    # Erosion
    # erosion = cv2.erode(mask, kernel, iterations=1)

    # Dilation
    # dilation = cv2.dilate(mask, kernel, iterations=1)

    # Морфологическое открытие и закрытие
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow('er', erosion)
    # cv2.imshow('dil', dilation)
    # cv2.imshow('open', opening)
    cv2.imshow('close', closing)
    cv2.imshow('frame' , frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()