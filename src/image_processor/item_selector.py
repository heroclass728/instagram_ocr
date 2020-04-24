import os
import cv2
import numpy as np

from settings import CUR_DIR


def convert_image_color(frame_path, file_name):

    new_path = os.path.join(CUR_DIR, 'temp_{}.jpg'.format(file_name))

    sharpening_kernel = np.array(([0, -1, 0], [-1, 5, -1], [0, -1, 0]), dtype="int")
    origin_frame = cv2.imread(frame_path)
    gray_frame = cv2.cvtColor(origin_frame, cv2.COLOR_BGR2GRAY)
    sharp_image = cv2.filter2D(gray_frame, -1, sharpening_kernel)
    # _, thresh_image = cv2.threshold(sharp_image, 210, 255, cv2.THRESH_BINARY)
    # cv2.imshow("thresh image", thresh_image)
    # cv2.imshow("sharpen image", sharp_image)
    # cv2.waitKey()
    cv2.imwrite(new_path, sharp_image)

    return new_path


def select_item(frame_path, region, items):

    frame = cv2.imread(frame_path, 0)
    frame_inv = cv2.bitwise_not(frame)
    sub_frames = []
    cnt_rets = []
    kernel = np.ones((2, 2), np.uint8)

    for i, reg in enumerate(region):
        sub_frame = frame_inv[reg[1]:reg[3], reg[0]:reg[2]]
        # cv2.imshow("sub frame", sub_frame)
        # cv2.waitKey()
        sub_frames.append(sub_frame)
        white_pixels = len(sub_frame[sub_frame > 250])
        if white_pixels != 0:
            cnt_rets.append(1)

    iteration_cnt = 1
    while len([x for x in cnt_rets if x == 1]) > 1:
        for i, sub_frame in enumerate(sub_frames):
            sub_frame = cv2.erode(sub_frame, kernel, iterations=iteration_cnt)
            # cv2.imshow("sub frame", sub_frame)
            # cv2.waitKey()
            white_pixels = len(sub_frame[sub_frame > 200])
            if white_pixels == 0:
                cnt_rets[i] = 0
        iteration_cnt += 1

    item = items[cnt_rets.index(1)]

    return item


if __name__ == '__main__':

    convert_image_color(frame_path="")
