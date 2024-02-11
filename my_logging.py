from params import *
import cv2


def show_logs(flag):
    print(f'Program that generates deg {deg} codes has been started!')
    if flag:
        print(f'\
        bool_generate_again = {bool_generate_again} \n\
        bool_draw_circle = {bool_draw_circle} \n\
        bool_save_codes = {bool_save_codes} \n\
        bool_show_log = {bool_show_log} \n\
        bool_save_pics = {bool_save_pics} \n\
        bool_prohibit = {bool_prohibit}')


def show(list, row):
    # row = 5
    n = len(list) / row
    temp = 0
    for elem in list:
        temp += 1
        if temp != row:
            print(elem, end=' ')
        else:
            temp = 0
            n -= 1
            print(elem)
    print('')


def show_me(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
