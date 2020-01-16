#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('selfie1', __name__,
                url_prefix='/selfie1',
                static_folder='static',
                )


@mod.route('/')
def index():
    return render_template(
        'images/selfie1.html'
    )
