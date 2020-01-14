#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient, GEO2D
from pymongo.errors import BulkWriteError
from goodfornothing.config import MongoConfig


_client = MongoClient(MongoConfig.HOST, MongoConfig.PORT)
_db = _client[MongoConfig.DATABASE]


def init_collection(session):
    _collection = _db[session]
    _collection.remove({})
    _collection.create_index([('loc', GEO2D)])


def write_idxs(arr, session):
    _collection = _db['idxs']
    _collection.delete_one(
        {'session': session},
    )
    _collection.insert_one(dict(
        session=session,
        idxs=[int(x) for x in arr]
    ))


def get_idx(idx, session):
    _collection = _db['idxs']
    _docs = _collection.find_one({
        'session': session
    })['idxs'][idx]
    return _docs


def del_idxs(idxs, session):
    _collection = _db['idxs']
    _docs = _collection.update(
        {'session': session},
        {'$pull': {'idx': {'$in': idxs}}},
    )
    return _docs


def get_shuffled_idxs(ordered_idxs, session_id):
    _collection = _db['idxs']
    _docs = _collection.find_one(dict(
        session=session_id,
    ))['idxs'][ordered_idxs[0]:ordered_idxs[-1]+1]
    return _docs


def write_pixel(x, y, c, session):
    _collection = _db[session]
    _collection.insert_one(dict(
        loc=[x, y], c=c
    ))


def write_pixels(pxls, session):
    _collection = _db[session]
    _requests = [dict(loc=[p['lon'], p['lat']], c=p['color'], idx=p['idx'])
                 for p in pxls]
    try:
        _collection.insert_many(_requests, ordered=False)
    except BulkWriteError as bwe:
        print(bwe.details)


def tint_pixels(idx, idxs, session):
    _collection = _db[session]

    # Update pixel colors
    _collection.update_many(
        {'idx': {'$in': idxs}},
        # {'$mul': {'c.$[]': .5}},
        [{'$set': {'c': {'$map': {
            'input': '$c',
            'in': {'$cond': {
                'if': {'$gte': ['$$this', 253]},
                'then': 255,
                'else': {'$add': ['$$this', {'$pow': [
                    {'$subtract': [255, '$$this']}, .67]}]}}}}}}}])

    # Get all white pixels
    white = _collection.find({
        # 'idx': {'$in': idxs},
        'c.0': {'$gte': 254},
        'c.1': {'$gte': 254},
        'c.2': {'$gte': 254},
    }, {'_id': 0})

    # Remove indices of white pixels from idxs collection
    _db['idxs'].update(
        {'session': session},
        {'$pull': {'idxs': {'$in': [f['idx'] for f in white]}}}
    )

    # Return pixels and length of idxs collection
    return (
        _collection.find({
            'idx': {'$in': idxs},
            }, {'_id': 0}),
        len(_db['idxs'].find_one({'session': session})['idxs']),
        idx,
        # len(_db['idxs'].find({'session': session})['idxs'])
    )


def get_nonwhite_n(session):
    return len(_db['idxs'].find_one({'session': session})['idxs'])


def get_near(lonlat, _n, session):
    _collection = _db[session]
    # _docs = _collection.find({'loc': {'$near': lonlat}}, {'_id': 0}).limit(5)
    _docs = _collection.aggregate([
        {'$geoNear': {'near': lonlat, 'distanceField': 'dist', 'minDistance': 0.00001 }},
        {'$limit': _n},
        {'$project': {'_id': 0}}
    ])
    return _docs


if __name__ == '__main__':
    pass
