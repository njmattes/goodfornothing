#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('walldrawing6114b', __name__,
                url_prefix='/walldrawing6114b',
                static_folder='static',
                )


@mod.route('/')
def index():
    return render_template(
        'images/walldrawing/walldrawing6114b.html'
    )
