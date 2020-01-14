#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('2017a', __name__,
                url_prefix='/2017a',
                static_folder='static',
                )


@mod.route('/')
def index():
    return render_template(
        'images/2017a.html'
    )
