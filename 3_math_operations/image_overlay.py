import cv2

img1 = cv2.imread('math_operations\mountains.jpg')
img2 = cv2.imread('math_operations\yandex_logo.png')


# resize
r1 = cv2.resize(img1, (720, 720))
r2 = cv2.resize(img2, (720, 720))

# Сумма матриц
# s = cv2.add(r1, r2)

# Вычитаение матриц
# s = cv2.subtract(r2, r1)

# Смешивание изображений (dst = img1*alpha + img2*beta + gamma)
s = cv2.addWeighted(r1, 1, r2, 0.2, 0)

cv2.namedWindow('add', cv2.WINDOW_NORMAL)
cv2.imshow('add', s)
# cv2.imwrite("math_operations/image_add_weighted.png", s)

cv2.waitKey(0)
cv2.destroyAllWindows()