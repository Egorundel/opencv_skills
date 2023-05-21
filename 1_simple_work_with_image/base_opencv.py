import cv2
import numpy as np

img = cv2.imread('for_test.jpg')

img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
img = cv2.GaussianBlur(img, (9, 9), 0)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.Canny(img, 250, 250)

kernel = np.ones((2,2), np.uint8)
img = cv2.dilate(img, kernel, iterations=2)
img = cv2.erode(img, kernel, iterations=1)

cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
cv2.imshow('Result', img)
cv2.imwrite("for_test_result.jpg", img)

cv2.waitKey(0)
