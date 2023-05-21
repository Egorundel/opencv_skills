import cv2
import numpy as np

def nothing():
    pass

# считываение видеопотока с веб-камеры
cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')

# создание ползунков
cv2.createTrackbar('HL', 'frame', 0, 180, nothing)
cv2.createTrackbar('SL', 'frame', 0, 255, nothing)
cv2.createTrackbar('VL', 'frame', 0, 255, nothing)

cv2.createTrackbar('H', 'frame', 0, 180, nothing)
cv2.createTrackbar('S', 'frame', 0, 255, nothing)
cv2.createTrackbar('V', 'frame', 0, 255, nothing)

while True:
    ret, frame = cap.read()

    # переход в пространство HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # использование ползунков для отсеивания нижней и верхней границ цвета в цветовом пространстве HSV
    hl = cv2.getTrackbarPos('HL', 'frame')
    sl = cv2.getTrackbarPos('SL', 'frame')
    vl = cv2.getTrackbarPos('VL', 'frame')

    h = cv2.getTrackbarPos('H', 'frame')
    s = cv2.getTrackbarPos('S', 'frame')
    v = cv2.getTrackbarPos('V', 'frame')

    lower = np.array([hl, sl, vl])
    upper = np.array([h, s, v])

    # маска по цвету
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # геометрические преобразования (поворот на 90 градусов по часовой стрелке)
    # res = cv2.rotate(res, cv2.ROTATE_90_CLOCKWISE)

    # увеличение изображения
    height, width = res.shape[:2]
    res = cv2.resize(res, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()