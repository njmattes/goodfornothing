#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('walldrawing1', __name__,
                url_prefix='/walldrawing1',
                static_folder='static',
                )


@mod.route('/')
def index():
    return render_template(
        'images/walldrawing/walldrawing1.html'
    )
