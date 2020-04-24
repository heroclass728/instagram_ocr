import os
import cv2
import numpy as np

from settings import CUR_DIR, HUE_THRESH, INV_THRESH


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


def get_main_color(frame, mask=None):

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # hsv_main_values = []
    # for i in range(1, 3):
    hue_hist = cv2.calcHist([hsv_frame], [1], mask, [256], [0, 256])
    hue_value = np.argmax(hue_hist)
    # hsv_main_values.append(main_value)

    return hue_value


def select_item(frame_path, region, items):

    frame = cv2.imread(frame_path)
    sub_frames = []
    cnt_rets = []
    hue_values = []
    item_index = None
    kernel = np.ones((2, 2), np.uint8)

    for reg in region:

        sub_frame = frame[reg[1]:reg[3], reg[0]:reg[2]]
        # cv2.imshow("sub frame", sub_frame)
        # cv2.waitKey()
        hue_value = get_main_color(frame=sub_frame)
        sub_frames.append(sub_frame)
        hue_values.append(hue_value)

    zero_ret = True
    for i, hue in enumerate(hue_values):
        if hue > HUE_THRESH:
            zero_ret = False
            item_index = i
            break

    if zero_ret:

        inv_sub_frames = []
        for sub_frame in sub_frames:
            sub_frame_gray = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
            sub_frame_inv = cv2.bitwise_not(sub_frame_gray)
            inv_sub_frames.append(sub_frame_inv)
            # cv2.imshow("sub frame", sub_frame)
            # cv2.waitKey()
            white_pixels = len(sub_frame_inv[sub_frame_inv > INV_THRESH])
            if white_pixels != 0:
                cnt_rets.append(1)
            else:
                cnt_rets.append(0)

        iteration_cnt = 1
        while len([x for x in cnt_rets if x == 1]) > 1:
            for i, sub_frame in enumerate(inv_sub_frames):
                sub_frame = cv2.erode(sub_frame, kernel, iterations=iteration_cnt)
                # cv2.imshow("sub frame", sub_frame)
                # cv2.waitKey()
                white_pixels = len(sub_frame[sub_frame > INV_THRESH])
                if white_pixels == 0:
                    cnt_rets[i] = 0
            iteration_cnt += 1
        item_index = cnt_rets.index(1)

    item = items[item_index]

    return item


if __name__ == '__main__':

    convert_image_color(frame_path="", file_name="")
