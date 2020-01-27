#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image
import json


def image_to_array(image):
    data = np.asarray(image, dtype=np.uint8)
    data = data[:, :, :]
    data.setflags(write=True)
    return data


def image_pair_to_json(image1_file, image2_file, json_file):

    def ab():
        speed_ab = np.empty(speed_a.shape)
        for i in range(speed_ab.shape[0]):
            speed_ab[i, :] = np.concatenate((
                speed_a[i, :diff_idx[i]], speed_b[i, diff_idx[i]:]))

        image_ab = np.empty(image_a.shape)
        for i in range(image_ab.shape[0]):
            image_ab[i, :, :] = np.concatenate((
                image_a[i, :diff_idx[i]], image_b[i, diff_idx[i]:]))

        return {
            t: [[s[0],
                 s[1],
                 image_ab[s[0], s[1]].tolist()]
                for s in np.argwhere(speed_ab == t)]
            for t in bins}

    def ba():
        speed_ba = np.empty(speed_a.shape)
        for i in range(speed_ba.shape[0]):
            speed_ba[i, :] = np.concatenate((
                speed_b[i, :diff_idx[i]], speed_a[i, diff_idx[i]:]))

        image_ba = np.empty(image_a.shape)
        for i in range(image_ba.shape[0]):
            image_ba[i, :, :] = np.concatenate((
                image_b[i, :diff_idx[i]], image_a[i, diff_idx[i]:]))

        return {
            t: [[s[0],
                 s[1],
                 image_ba[s[0], s[1]].tolist()]
                for s in np.argwhere(speed_ba == t)]
            for t in bins}

    image1 = Image.open(os.path.join('../static', 'images', image1_file))
    image2 = Image.open(os.path.join('../static', 'images', image2_file))

    image_a = image_to_array(image1)
    image_b = image_to_array(image2)
    image_diff = np.abs(image_a - image_b)

    speed = np.sum(image_diff, axis=2, dtype=np.float32)
    speed[speed == 0] = 1
    speed = np.divide(speed, np.max(speed))
    speed = np.power(speed, 2)

    speed_shape = speed.shape
    longest_duration = 3000

    speed = np.round(speed * longest_duration, 0)
    speed_a = np.cumsum(speed, axis=1)
    speed_b = np.cumsum(np.fliplr(speed), axis=1)

    bins = np.linspace(0, longest_duration, 21)
    bins = np.arange(0, np.max(speed_a) + bins[1], bins[1])

    digitized_idx_a = np.digitize(speed_a.ravel(), bins, right=True)
    digitized_idx_b = np.digitize(speed_b.ravel(), bins, right=True)
    speed_a = bins[digitized_idx_a].reshape(speed_shape)
    speed_b = bins[digitized_idx_b].reshape(speed_shape)
    speed_b = np.fliplr(speed_b)

    speed_diff = np.abs(speed_a - speed_b)
    diff_idx = np.argmin(speed_diff, axis=1)

    ab = ab()
    ba = ba()
    a = {t: [[s[0],
              s[1],
              image_a[s[0], s[1]].tolist()]
             for s in np.argwhere(speed_a == t)]
         for t in bins}
    b = {t: [[s[0],
              s[1],
              image_b[s[0], s[1]].tolist()]
             for s in np.argwhere(speed_b == t)]
         for t in bins}

    json_data = dict()
    json_data['idx'] = bins.tolist()
    # json_data['ab'] = ab
    # json_data['ba'] = ba
    json_data['a'] = a
    json_data['b'] = b

    json_file = os.path.join('../static', 'json', json_file)
    with open(json_file, 'w') as f:
        json.dump(json_data, f)


if __name__ == '__main__':
    image_pair_to_json(
        'tiananmen_sm.png',
        'selfie_stick_sm.png',
        'tiananmen_selfie_400x300_2.json',
    )
