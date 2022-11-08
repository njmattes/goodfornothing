#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import floor
from random import randint
from datetime import datetime
import numpy as np
from PIL import Image
from marios.dk import MARIO, COLORS
from scaler import scale_pixels
from neighbors import neighbors


canvas = np.empty((1920, 1080))


def glitch_walk(walking_mario, offset=6, ops=1000, seq=0,
                video_width=1920, video_height=1080, pixel_width=30):

    height, width = walking_mario.shape

    for n in range(ops):
        idxa = np.array([randint(1, height - 2), randint(1, width - 2)])
        idxb = idxa + neighbors[randint(0, len(neighbors) - 1)]

        pxla = walking_mario[tuple(idxa)]
        pxlb = walking_mario[tuple(idxb)]
        walking_mario[tuple(idxa)] = pxlb
        walking_mario[tuple(idxb)] = pxla

    scale = pixel_width
    shp = (video_width, video_height)

    arr = scale_pixels(walking_mario, scale)

    img = Image.new('RGB', shp, 'white')  # Create a new black image
    pixels = img.load()  # Create the pixel map
    for i in range(width * scale):    # For every pixel:
        for j in range(height * scale):
            pxl = COLORS[arr[j][i]]  # Set the colour accordingly
            pixels[(offset * scale + i) % shp[0], 270 + j] = pxl

    img.save('../output/5/MARIO-dk-{:04d}-{}-{}.png'.format(seq, ops, datetime.now()))


def make_some_frames(start_n, n_frames, max_n, idx, offset=26, gradient=1,
                     video_width=1920, video_height=1080, pixel_width=30):
    from marios.dk import WALK1
    from marios.dk import WALK2

    idx += 1

    for i in range(n_frames):

        if gradient == 1:
            n = start_n + i + 1
        elif gradient == -1:
            n = start_n - i - 1



        if n == 1 or n == max_n:
            walking_mario = MARIO.copy()
        else:
            if n % 2 == 0:
                walking_mario = WALK1.copy()
            else:
                walking_mario = WALK2.copy()

        width = video_width / pixel_width
        if offset >= width:
            offset = offset % width

        if gradient == 1 and i == 0:
            ops = 0
        else:
            exp = (max_n - abs(2 * n - max_n)) / max_n
            ops = int(1000 ** exp)
        print('index {}, n {}, grad {}, ops {}'.format(i, n, gradient, ops))
        glitch_walk(walking_mario, offset, ops, idx+i,
                    video_width, video_height, pixel_width)
        offset += 5

    return n, offset, idx + i


def make_all_frames():
    max_n = 1024
    idx = 0

    start_n, offset, idx = make_some_frames(0, max_n//2, max_n, idx)
    start_n, offset, idx = make_some_frames(start_n, max_n//2, max_n, idx, offset, -1)
    start_n, offset, idx = make_some_frames(0, 1, 1, idx)
    # start_n, offset, idx = make_some_frames(start_n, 30, max_n, idx, offset, 1)
    # start_n, offset, idx = make_some_frames(start_n, 10, max_n, idx, offset, -1)
    # start_n, offset, idx = make_some_frames(start_n, 22, max_n, idx, offset, 1)
    # start_n, offset, idx = make_some_frames(start_n, 64, max_n, idx, offset, -1)


def make_walking_video():
    import cv2
    import os

    image_folder = '../output/5'
    video_name = 'video.avi'

    images = [img for img in sorted(os.listdir(image_folder)) if img.endswith('.png')]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    four_cc = cv2.VideoWriter_fourcc(*'MJPG')

    video = cv2.VideoWriter(
        video_name,
        four_cc,
        8,
        (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    # from marios.dk import WALK1
    # glitch_walk(WALK1, 0, 0)
    # make_frames(128)
    make_walking_video()
    # make_all_frames()
