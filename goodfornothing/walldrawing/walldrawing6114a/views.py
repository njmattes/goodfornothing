#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('walldrawing6114a', __name__,
                url_prefix='/walldrawing6114a',
                static_folder='static',
                )


@mod.route('/')
def index():
    return render_template(
        'images/walldrawing/walldrawing6114a.html'
    )
