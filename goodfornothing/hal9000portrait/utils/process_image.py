#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image


def foo():
    im = Image.open(os.path.join('src', 'yellowSaturation.png'))
    data = np.asarray(im, dtype=np.uint8)
    g = data[:, :, 1]
    g = np.roll(g, 1, axis=1)
    new_data = np.stack((
        np.sort(data[:, :, 0], axis=0),
        np.sort(data[:, :, 1], axis=0),
        np.sort(data[:, :, 2], axis=0),
        # np.roll(data[:, :, 1], 1, axis=1),
        # np.roll(data[:, :, 2], 2, axis=1),
    ), axis=2)
    print(new_data.shape)
    im2 = Image.fromarray(new_data, 'RGB')
    im2.save('src/yellowSaturation4.png')


def bar():
    imh = Image.open(os.path.join('src', 'yellowSaturation3.png'))
    imv = Image.open(os.path.join('src', 'yellowSaturation4.png'))
    datah = np.asarray(imh, dtype=np.uint8) / 255.
    datav = np.asarray(imv, dtype=np.uint8) / 255.
    print(datah)
    print(datav)
    new_data = (datah * datav) * 255.
    im2 = Image.fromarray(new_data, 'RGB')
    im2.save('src/yellowSaturation5.png')


def hal_to_csv():
    im = Image.open(os.path.join('static', 'images', 'hal_sm.png'))
    data = np.asarray(im, dtype=np.uint8)
    data = data[:, :, :]
    data.setflags(write=True)
    # print(data)
    # map(np.random.shuffle, data)
    with open(os.path.join('static', 'csv', 'hal_rows.csv'), 'w') as f:
        f.write('color,duration,transition,ease\n')
        for a in range(data.shape[0]):
            for b in range(data.shape[1]):
                f.write('"rgb({})",10,10,easeLinear\n'.format(
                    ','.join([str(x) for x in data[a, b, :]])))


if __name__ == '__main__':
    # bar()
    hal_to_csv()
