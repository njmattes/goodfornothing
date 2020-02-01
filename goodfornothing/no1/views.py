#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from math import floor
import numpy as np
from flask import Blueprint, render_template, session, Response
from goodfornothing.no1.mongo import init_collection
from goodfornothing.no1.mongo import write_idxs
from goodfornothing.no1.mongo import write_pixels
from goodfornothing.no1.mongo import get_shuffled_idxs
from goodfornothing.no1.mongo import tint_pixels
from goodfornothing.no1.mongo import get_near


mod = Blueprint('no1', __name__,
                url_prefix='/no1',
                static_folder='static',
                template_folder='templates',
                )


@mod.route('/')
@mod.route('/color/<cg>')
@mod.route('/color/<cg>/<int:size>')
@mod.route('/color/<cg>/<int:size>/<int:number>')
@mod.route('/color/<cg>/<int:size>/<int:number>/<int:timer>')
@mod.route('/color/<cg>/<int:size>/<int:number>/<int:timer>/<int:threshold>')
@mod.route('/color/<cg>/<int:size>/<int:number>/<int:timer>/<int:threshold>/'
           '<int:network>')
@mod.route('/color/<cg>/size/<int:size>/number/<int:number>/timer/<int:timer>/'
           'threshold/<int:threshold>/network/<int:network>')
def index(cg='g', size=20, number=10, timer=20, threshold=30, network=3):
    return render_template(
        'images/no1.html',
        size=size,
        number=number,
        timer=timer,
        threshold=threshold,
        network=network,
        cg=cg,
    )


@mod.route('/init/<int:width>/<int:height>')
def init(width, height):
    session['width'] = width
    session['height'] = height
    session['area'] = width * height
    arr = np.arange(session['area'])
    np.random.shuffle(arr)
    init_collection(session.sid)
    write_idxs(arr, session.sid)
    return Response(
        json.dumps({'success': True}),
        200,
        {'ContentType': 'application/json'}
    )


@mod.route('/get_gpxl/<int:idx>,<int:n>/<int:threshold>/<int:network>')
def get_gpxl(idx, n, threshold, network):
    ordered_idxs = np.arange(idx, idx + n)
    shuffled_idxs = get_shuffled_idxs(ordered_idxs, session.sid)
    pxl_dicts = get_pxl_dicts(shuffled_idxs, ordered_idxs, threshold, network,
                              session.sid)
    write_pixels(pxl_dicts, session.sid)
    return Response(
        json.dumps({'pxls': pxl_dicts}),
        mimetype='application/json',
    )


@mod.route('/get_cpxl/<int:idx>,<int:n>/<int:threshold>/<int:network>')
def get_cpxl(idx, n, threshold, network):
    ordered_idxs = np.arange(idx, idx+n)
    shuffled_idxs = get_shuffled_idxs(ordered_idxs, session.sid)
    pxl_dicts = get_pxl_dicts(shuffled_idxs, ordered_idxs, threshold, network,
                              session.sid, grey=False)
    write_pixels(pxl_dicts, session.sid)
    return Response(
        json.dumps({'pxls': pxl_dicts}),
        mimetype='application/json',
    )


@mod.route('/get_half_pxls/<int:idx>,<int:n>/<int:threshold>/<int:network>')
def get_half_pxl(idx, n, threshold, network):
    ordered_idxs = np.arange(idx, idx+n)
    shuffled_idxs = get_shuffled_idxs(ordered_idxs, session.sid)
    foo = tint_pixels(idx, shuffled_idxs, session.sid)
    return Response(
        json.dumps({'pxls': [
            {'xy': get_xy(f['idx']),
             'color': f['c']}
            for f in foo[0]],
            'n': foo[1],  # Number of indexes left to tint
            't': foo[2],  # Current index in loop
        }),
        mimetype='application/json',
    )


@mod.route('/get_nonwhite_n')
def get_nonwhite_n():
    from boi.mongo import get_nonwhite_n
    return Response(
        json.dumps({'n': get_nonwhite_n(session.sid)}),
        mimetype='application/json',
    )


def get_xy(idx):
    """Given the index of a point, retrieves it's (x, y)
    coordinate given the width of the matrix stored in the session.

    :param idx: The index of the pixel whose coordinates you wish to calculate
    :type idx: int
    :return: The (x, y) coordinates of the point
    :rtype: tuple
    """
    w = session['width']
    x = idx % w
    y = floor(idx / w)
    return x, y


def get_xys(s_idxs):
    """Given the indices of a list of points, retrieves their (x, y)
    coordinates given the width of the matrix stored in the session.

    :param s_idxs: Indices of the pixel whose coordinates you wish to calculate
    :type s_idxs: list
    :return: A list of (x, y) coordinates of the points
    :rtype: list[tuple]
    """
    return [get_xy(idx) for idx in s_idxs]


def scale_coord(_coord, _p=1.0):
    """Computes the scaled coordinate of a point, based on either
     a x or y coordinate, suitable for storing in Mongo. Mongo's 2D
     index requires that points be in the range ((-180, 180), (-90, 90)).
     Optionally this value can be scaled by _p, which will stretch
     the coloring either horizontally (_p > 1), or vertically (_p < 1).
    # TODO: Check that the GEO2D index is the correct one to be using.

    :param _coord: A single x or y coordinate of the point
    :type _coord: float
    :param _p: Scaling factor
    :type _p: float
    :return: The scaled coordinate
    :rtype: float
    """
    _w = session['width']
    _h = session['height']
    return (_coord / max(_w, _h)) * 10 * _p


def get_pxl_dicts(shuffled_idxs, ordered_idxs, threshold, network,
                  sid, grey=True):
    """Creates a dictionary representation of the pixel for inserting
    into Mongo.

    :param shuffled_idxs: The indices of the pixels
    :type shuffled_idxs: list
    :param ordered_idxs: The indices of the operations in the loop
    :type ordered_idxs: list
    :param sid: The ID of the flask session
    :type sid: str
    :param grey: Whether to return a grey value or color value
    :type grey: bool
    :return: Dictionary of pixel properties
    :rtype: dict
    """

    def get_color(xy, i):
        _color = [None, None, None]
        if ordered_idxs[i] > _a / threshold:
            _color = get_average_color(
                [scale_coord(xy[0]),
                 scale_coord(xy[1])],
                network,
                sid)
        else:
            _color = get_random_color(grey=grey)
        return _color

    _a = session['area']
    _p = 1  # proportion, less than 1 stretches vertically, \
    # more than 1 stretches horizontally
    return [
        dict(
            xy=xy,
            lon=scale_coord(xy[0]),
            lat=scale_coord(xy[1]),
            color=get_color(xy, i),
            idx=shuffled_idxs[i],
        ) for i, xy in enumerate(get_xys(shuffled_idxs))
    ]


def get_average_color(lonlat, network, sid):
    """Blend the colors of the pixels nearest the target pixel.

    :param lonlat: The scaled (x, y) coordinates of the pixel in Mongo
    :type lonlat: list
    :param sid: The ID of the session
    :type sid: str
    :return: The RGB representation of the blended color
    :rtype: list
    """

    # Build a 5 by 6 matrix of the nearest points. Each row is
    # a point. Each row contains [lon, lat, r, g, b, dist]
    nears = np.array([
        np.array(
            [n['loc'][0], n['loc'][1],
             n['c'][0], n['c'][1], n['c'][2],
             1 / n['dist']])
        for n in get_near(lonlat, network, sid)])
    # Weight the average of the color components by the distance
    # from the target pixel.
    return ((nears[:, 5] / nears[:, 5].sum()).reshape(
        (nears.shape[0], -1)) * nears[:, 2:]).sum(axis=0).tolist()


def get_random_color(grey=True):
    if grey:
        r = 64
        return (np.ones(3) * np.random.randint(248 - r, 248)).tolist()
    return np.array([
        np.random.randint(200, 230),
        np.random.randint(230, 255),
        np.random.randint(220, 255), ]).tolist()
