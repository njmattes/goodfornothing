#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from math import floor
from random import randint
from datetime import datetime
import numpy as np
from PIL import Image
from marios.dk import MARIO, COLORS
from scaler import scale_pixels
from neighbors import neighbors


def glitcher(N=1000):
    height, width = MARIO.shape

    for n in range(N):
        idxa = np.array([randint(1, height - 2), randint(1, width - 2)])
        idxb = idxa + neighbors[randint(0, len(neighbors) - 1)]

        pxla = MARIO[tuple(idxa)]
        pxlb = MARIO[tuple(idxb)]
        MARIO[tuple(idxa)] = pxlb
        MARIO[tuple(idxb)] = pxla

    scale = 33
    shp = np.array(tuple(reversed(MARIO.shape))) * scale
    shp = tuple(shp)

    arr = scale_pixels(MARIO, scale)
    shp = tuple(reversed(arr.shape))

    img = Image.new('RGB', shp, 'white')  # Create a new black image
    pixels = img.load()  # Create the pixel map
    for i in range(shp[0]):    # For every pixel:
        for j in range(shp[1]):
            pxl = COLORS[arr[j][i]]  # Set the colour accordingly
            pixels[i, j] = pxl


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
    img.save('../output/3/MARIO-dk-{}-{}.png'.format(N, datetime.now()))
    # img.show()


if __name__ == '__main__':
    for n in [0, 1, 2, 3, 4, 5, 6, 7, 10, 13, 17, 23, 31, 41, 54, 72, 96,
              127, 170, 226, 300, 399, 531, 706, 1000]:
        glitcher(n)
