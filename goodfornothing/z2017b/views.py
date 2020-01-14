#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('2017b', __name__,
                url_prefix='/2017b',
                static_folder='static',
                )


@mod.route('/')
def index():
    return render_template(
        'images/2017b.html'
    )
