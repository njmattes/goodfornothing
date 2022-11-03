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


def glitch_walk(walking_mario, offset=6, N=1000):
    height, width = walking_mario.shape

    for n in range(N):
        idxa = np.array([randint(1, height - 2), randint(1, width - 2)])
        idxb = idxa + neighbors[randint(0, len(neighbors) - 1)]

        pxla = walking_mario[tuple(idxa)]
        pxlb = walking_mario[tuple(idxb)]
        walking_mario[tuple(idxa)] = pxlb
        walking_mario[tuple(idxb)] = pxla

    scale = 30
    shp = (1920, 1080)

    arr = scale_pixels(walking_mario, scale)

    img = Image.new('RGB', shp, 'white')  # Create a new black image
    pixels = img.load()  # Create the pixel map
    for i in range(15*30):    # For every pixel:
        for j in range(18*30):
            pxl = COLORS[arr[j][i]]  # Set the colour accordingly
            pixels[(offset*scale+i)%1920, 270+j] = pxl


    # img = Image.new('RGB', shp, 'white')  # Create a new black image
    # pixels = img.load()  # Create the pixel map
    # for i in range(shp[0]):    # For every pixel:
    #     for j in range(shp[1]):
    #         ii = floor(i/scale)
    #         jj = floor(j/scale)
    #         pxl = COLORS[MARIO[jj][ii]]  # Set the colour accordingly
    #         pixels[i, j] = pxl



    # img.save('MARIOa.png')
    # img.save('../output/1/MARIO-dk-{}-{}.png'.format(N, datetime.now()))
    img.save('../output/4/MARIO-dk-{}-{}.png'.format(N, datetime.now()))
    # img.show()


def make_frames():
    from marios.dk import WALK1
    from marios.dk import WALK2

    offset = 0
    walking_mario = WALK2

    for n in range(15):
        width = 1920 / 30
        if n > 0:
            if n % 2 == 0:
                walking_mario = WALK2
                offset += 4
            else:
                walking_mario = WALK1
                offset += 6
        if offset >= width:
            offset = offset % width
        glitch_walk(walking_mario, offset, n)


def make_walking_video():
    import cv2
    import os

    image_folder = 'images'
    video_name = 'video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    # from marios.dk import WALK1
    # glitch_walk(WALK1, 0, 0)
    make_frames()
