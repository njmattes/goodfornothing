#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import numpy as np
from PIL import Image


def json_to_image(json_file):
    json_file = os.path.join('../static', 'json', json_file)
    with open(json_file, 'r') as f:
        data = json.load(f)
        a = np.array(data['a'])
        b = np.array(data['b'])
        diff = np.array(data['diff'])
        speed = np.sum(diff, axis=2) / (255 * 3.)
        speed_ltr = np.cumsum(1. / speed, axis=1)
        speed_rtl = np.cumsum(1. / np.fliplr(speed), axis=1)
        speed_diff = np.abs(speed_ltr - np.fliplr(speed_rtl))
        diff_idx = np.argmin(speed_diff, axis=1)
        new_data = np.empty(a.shape)
        for i in range(new_data.shape[0]):
            new_data[i, :, :] = np.concatenate((
                a[i, :diff_idx[i]], b[i, diff_idx[i]:]))
        new_data = np.array(new_data, dtype=np.uint8)
        image = Image.fromarray(new_data, 'RGB')
        image.save(os.path.join('../static', 'images', 'tiananmen_selfie2.png'))



if __name__ == '__main__':
    json_to_image('tiananmen_selfie_400x300.json')
