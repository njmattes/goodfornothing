#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from glob import glob
import itertools
import numpy as np
import imageio as im
from skimage.util import view_as_windows
from sklearn.cluster import KMeans


class WallImages(object):
    def __init__(self, _dir):
        self.n = 16
        self.dir = os.path.abspath(_dir)
        self.image_files = glob(os.path.join(self.dir, '*.png'))
        self.height, self.width, self.depth = \
            im.imread(self.image_files[0]).shape
        self.indexes, self.centers = self._get_clustered_color_data(
            self._get_color_data()
        )
        self.indexes = self.get_indexes()
        self.h_prob = dict()
        self.v_prob = dict()

    def _get_color_data(self):
        image_files = glob(os.path.join(self.dir, '*.png'))
        arr = np.empty((len(image_files) * self.height * self.width, self.depth))
        for i, img in enumerate(self.image_files):
            img_data = im.imread(img)
            a = img_data.reshape((-1, self.depth))
            arr[i*len(a):(i+1)*len(a), :] = a
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
        self.build_probs_dicts()
        for w in self.get_windows():
            for idx in self.match_window(w):
                val = [int(self.indexes[idx[0]+1, idx[1]+1])]
                if len(val) > 0:
                    d = self.h_prob
                    for n in [0, 1, 2]:
                        if w[n] not in d.keys():
                            d[int(w[n])] = {} if n < 2 else []
                        d = d[w[n]]
                self.h_prob[w[0]][w[1]][w[2]] += [int(self.indexes[idx[0]+1, idx[1]+1])]
        for i, row in enumerate(self.indexes[:-1, :]):
            for j, n in enumerate(row):
                self.v_prob[int(n)] += [int(self.indexes[i+1, j])]


if __name__ == '__main__':
    iw = WallImages('../src/input_32')
    iw.probability()
    if not os.path.exists('{}'.format(iw.n)):
        os.mkdir('{}'.format(iw.n))
    # with open('{}/horizontal_probability.json'.format(iw.n), 'w') as f:
    #     f.write(json.dumps(iw.h_prob))
    # with open('{}/vertical_probability.json'.format(iw.n), 'w') as f:
    #     f.write(json.dumps(iw.v_prob))
    # with open('{}/color_centers.json'.format(iw.n), 'w') as f:
    #     f.write(json.dumps(
    #         {'colors': [[int(x) for x in c] for c in iw.centers]}))
    print(iw.indexes)
    print(np.random.randint(0, iw.indexes.shape[1], 10))
    print(iw.indexes[:, np.random.randint(0, iw.indexes.shape[1], 10)])
    with open('{}/all_vars.json'.format(iw.n), 'w') as f:
        f.write(json.dumps(
            {'HORIZ': iw.h_prob,
             'VERT': iw.v_prob,
             'COLORS': {
                 i: [int(x) for x in c] for i, c in enumerate(iw.centers)
             },
             'INIT': [
                 [int(x) for x in r]
                 for r in iw.indexes[:,
                          np.random.randint(0,
                                            iw.indexes.shape[1], 10)].T

             ]}))

    # print(props.shape)
