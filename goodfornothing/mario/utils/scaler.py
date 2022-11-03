#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def scale_pixels(arr, scale=10):
    # shp = np.array(tuple(reversed(MARIO.shape))) * scale
    # shp = tuple(shp)

    dims = arr.shape
    arr = np.repeat(arr[:, :, np.newaxis], scale).reshape(
        (dims[0], dims[1] * scale))
    arr = np.tile(arr, scale).reshape((dims[0] * scale, dims[1] * scale))
    return arr
