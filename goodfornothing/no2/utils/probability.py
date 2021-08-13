#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from glob import glob
from math import floor
import itertools
import numpy as np
import imageio as im
from skimage.util import view_as_windows
from skimage.transform import resize
from sklearn.cluster import KMeans


class HorizonImages(object):
    def __init__(self, _dir):
        self.n = 16
        self.dir = os.path.abspath(_dir)
        self.image_files = glob(os.path.join(self.dir, '*.tif'))
        self.image_file = im.imread(self.image_files[0])
        self.height, self.width, self.depth = self.image_file.shape
        SCALE = 50
        self.image_file = resize(self.image_file, (self.height // SCALE,
                                                   self.width // SCALE))
        self.height, self.width, self.depth = self.image_file.shape
        self.indexes, self.centers = self._get_clustered_color_data(
            self._get_color_data()
        )
        self.indexes = self.get_indexes()
        self.h_prob = dict()
        self.v_prob = dict()

    def _get_color_data(self):
        # image_files = glob(os.path.join(self.dir, '*.png'))
        arr = self.image_file.reshape((-1, self.depth))
        return arr

    def _get_clustered_color_data(self, arr):
        kmeans = KMeans(n_clusters=self.n)
        kmeans = kmeans.fit(arr)
        return kmeans.predict(arr), kmeans.cluster_centers_

    def get_indexes(self):
        idxs = self.indexes.reshape((self.height, -1))
        idxs = np.vstack((idxs[0, :], idxs, idxs[-1, :]))
        return idxs

    def get_windows(self):
        # return itertools.combinations_with_replacement(
        #     np.arange(self.n), 3)
        return itertools.product(np.arange(self.n), repeat=3)

    def build_probs_dicts(self):
        for n in range(self.n):
            if n not in self.v_prob:
                self.v_prob[int(n)] = []

    def match_window(self, window):
        match = np.array(window).reshape((3, -1))
        windows = view_as_windows(
            self.indexes[:, :-1], match.shape)
        return np.array((windows == match).all(axis=(2, 3)).nonzero()).T

    def probability(self):
        sea = np.zeros((16, 16, 16, 16))
        sky = np.zeros((16, 16, 16, 16))
        vert = np.zeros((10, 16))
        for i in range(self.height // 2 - 1):
            for j in range(1, self.width - 2):

                a, b, c = j - 1, j, j + 1
                y = self.height - i

                sea[self.indexes[y, a],
                    self.indexes[y, b],
                    self.indexes[y, c],
                    self.indexes[y - 1, b]] += 1

                sky[self.indexes[i, a],
                    self.indexes[i, b],
                    self.indexes[i, c],
                    self.indexes[i + 1, b]] += 1

                vert[floor((i + 1) / self.height * 10),
                     self.indexes[i + 1, b]] += 1
                vert[floor((y - 1) / self.height * 10),
                     self.indexes[y - 1, b]] += 1

        exponent = 1.5
        sea[(sea == 0).all(axis=-1)] = .00001
        sky[(sky == 0).all(axis=-1)] = .00001
        sea = sea ** exponent
        sky = sky ** exponent
        sea /= sea.sum(axis=-1).reshape((16, 16, 16, -1))
        sky /= sky.sum(axis=-1).reshape((16, 16, 16, -1))
        vert /= vert.sum(axis=-1).reshape((10, -1))
        colors = (self.centers * 255) // 1

        with open('../static/js/app/horizon_exp{}.json'.format(exponent), 'w') as f:
            json.dump({'colors': colors.tolist(),
                       'sea': sea.tolist(),
                       'sky': sky.tolist(),
                       'vert': vert.tolist(), }, f)


if __name__ == '__main__':
    iw = HorizonImages('../src')
    iw.probability()
