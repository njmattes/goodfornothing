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


mod = Blueprint('exhibition', __name__,
                url_prefix='/exhibition',
                static_folder='static',
                template_folder='templates',
                )


@mod.route('/')
def index():
    return render_template(
        'exhibition/index.html',
    )
