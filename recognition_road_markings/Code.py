import cv2
import numpy as np

cap = cv2.VideoCapture('video.mp4')

if cap.isOpened() == False:
    print('Нет возможности открыть видео')
    exit()

# img_size = [200, 360]

# Размеры трапеции
src = np.float32([[40, 540],
                  [920, 540],
                  [640, 350],
                  [320, 350]])
src_draw = np.array(src, dtype=np.int32)

# Размеры 
dst = np.float32([[0, 540],
                  [960, 540],
                  [960, 0],
                  [0, 0]])

while (cv2.waitKey(1) != 27):
    ret, frame = cap.read()
    if ret==False:
        print('Конец видео')
        break
    
    resized = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
    cv2.imshow('frame', resized)

    # Проводим бинаризацию по синему каналу изображения
    b_channel = resized[:,:,0]
    binary=np.zeros_like(b_channel)
    binary[(b_channel>120)]=255
    # cv2.imshow('b_channel', binary)

    # Проводим бинаризацию по порогу светлости изображения
    hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
    s_channel = resized[:,:,2]
    binary2=np.zeros_like(s_channel)
    binary2[(s_channel>130)]=1
    # cv2.imshow('s_channel', binary2)

    # "Соединяем" бинаризации. Если хотя бы в одном из Ч/Б изображений пиксель равен 1, то на конечном изображении этот пиксель мы делаем равным белому, а все остальные будут чёрными (нулями)
    allBinary = np.zeros_like(binary)
    allBinary[((binary==1)|(binary2==1))] = 255
    cv2.imshow('allBinary', allBinary)

    # Рисуем трапецию
    allBinary_visual = allBinary.copy()
    cv2.polylines(allBinary_visual, [src_draw], True, 255)
    cv2.imshow('polygon', allBinary_visual)

    # Рассчитываем матрицу преобразования
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(allBinary, M, (frame.shape[1]//2, frame.shape[0]//2), flags=cv2.INTER_LINEAR)
    cv2.imshow('warped', warped)

    # Теперь нам нужно найти самые белые столбцы в нижней части изображения, чтобы от них распологать окна для поиска линий разметки. Для этого посчитаем сумму чисел, отвечающих за цвет пикселя в каждом столбце.
    histogram = np.sum(warped[warped.shape[0]//2:,:], axis = 0)
    
    # Далее нам нужно определить номер самого белого стоолбца в правой и левой частях
    midpoint = histogram.shape[0]//2
    IndWhitestColumnL = np.argmax(histogram[:midpoint])
    IndWhitestColumnR = np.argmax(histogram[midpoint:]) + midpoint
    warped_visual = warped.copy()
    cv2.line(warped_visual, (IndWhitestColumnL, 0), (IndWhitestColumnL, warped_visual.shape[0]), 110, 2)
    cv2.line(warped_visual, (IndWhitestColumnR, 0), (IndWhitestColumnR, warped_visual.shape[0]), 110, 2)
    cv2.imshow("WhitestColumn", warped_visual)

    # Распологаем окна для поиска пикселей разметки
    nWindows = 20
    window_height = np.int(warped.shape[0]/nWindows)
    window_half_width = 40

    # Центр левого и правого окна
    XCenterLeftWindow = IndWhitestColumnL
    XCenterRightindow = IndWhitestColumnR

    # координаты (массив) для левой и правой линии разметки
    left_line_inds = np.array([], dtype=np.int16)
    right_line_inds = np.array([], dtype=np.int16)

    # Делаем из одноканального изображения трехканальное
    out_img = np.dstack((warped, warped, warped))

    # Получаем индексы всех белых пикселей на изображении
    nonzero = warped.nonzero()
    WhitePixelIndY = np.array(nonzero[0])
    WhitePixelIndX = np.array(nonzero[1])

    # Вычисляем координаты углов окон и считаем какие пиксели в эти окна попадают
    for window in range(nWindows):
        
        win_y1 = warped.shape[0] - (window+1) * window_height
        win_y2 = warped.shape[0] - (window) * window_height

        left_win_x1 = XCenterLeftWindow - window_half_width
        left_win_x2 = XCenterLeftWindow + window_half_width
        right_win_x1 = XCenterRightindow - window_half_width
        right_win_x2 = XCenterRightindow + window_half_width
        
        # Рисование окон
        cv2.rectangle(out_img, (left_win_x1, win_y1), (left_win_x2, win_y2), (50 + window*21, 0, 0), 2)
        cv2.rectangle(out_img, (right_win_x1, win_y1), (right_win_x2, win_y2), (0, 0, 50 + window*21), 2)
        cv2.imshow('windows', out_img)

        # Получаем индексы белых пикселей, попавших в окна
        good_left_inds = ((WhitePixelIndY >= win_y1) & (WhitePixelIndY <= win_y2) & 
                          (WhitePixelIndX >= left_win_x1) & (WhitePixelIndX <= left_win_x2)).nonzero()[0]

        good_right_inds = ((WhitePixelIndY >= win_y1) & (WhitePixelIndY <= win_y2) & 
                          (WhitePixelIndX >= right_win_x1) & (WhitePixelIndX <= right_win_x2)).nonzero()[0]

        # Допишем эти индексу к массиву, в котором мы храним индексы для всей левой и правой линий
        left_line_inds = np.concatenate((left_line_inds, good_left_inds))
        right_line_inds = np.concatenate((right_line_inds, good_right_inds))

        # Если индексов белых пикселей в окне больше 50, то двигаем окно. Если нет, то не двигаем
        if len(good_left_inds) > 50:
            XCenterLeftWindow = np.int(np.mean(WhitePixelIndX[good_left_inds]))
        if len(good_right_inds) > 50:
            XCenterRightindow = np.int(np.mean(WhitePixelIndX[good_right_inds]))

    # Перекрасим в выводимом изображении заполненные нами пиксели
    out_img[WhitePixelIndY[left_line_inds], WhitePixelIndX[left_line_inds]] = [255, 0, 0]
    out_img[WhitePixelIndY[right_line_inds], WhitePixelIndX[right_line_inds]] = [0, 0, 255]
    cv2.imshow('Line', out_img)

    leftx = WhitePixelIndX[left_line_inds]
    lefty = WhitePixelIndY[left_line_inds]

    rightx = WhitePixelIndX[right_line_inds]
    righty = WhitePixelIndY[right_line_inds]

    # Проводим параболу между нашими левыми и правыми столбцами
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    center_fit = ((left_fit+right_fit)/2)

    for ver_ind in range(out_img.shape[0]):
        gor_ind = ((center_fit[0]) * (ver_ind ** 2) + center_fit[1] * (ver_ind) + center_fit[2])
        cv2.circle(out_img, (int(gor_ind), int(ver_ind)), 2, (255, 0, 255), 1)
    cv2.imshow("CenterLine", out_img)

print(resized.shape)
print(np.zeros_like(binary))
print('Гистограмма', histogram)
print('Матрица', M)
print('warped', warped)
