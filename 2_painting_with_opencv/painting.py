import cv2
import numpy as np

img = np.zeros((900,900,3), np.uint8)

# Линия
img = cv2.line(img, (10,10), (720, 640), (140, 160, 180), 5)

# Прямоугольник
img = cv2.rectangle(img, (10,10), (720, 640), (140, 160, 180), 5)

# Окружность
img = cv2.circle(img, (500, 450), 100, (255,0,0), -1)
img = cv2.circle(img, (500, 450), 100, (0,0,255), 5)

# Текст
cv2.putText(img, "Hello, World", (10, 750), 4, 3, (255,255,255), 3, cv2.LINE_AA)

cv2.imshow('image' , img)
cv2.imwrite("painting_with_opencv/painting_result.png", img)

cv2.waitKey(0)
cv2.destroyAllWindows()