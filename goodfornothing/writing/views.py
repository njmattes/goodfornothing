#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


writing = Blueprint(
    'writing', __name__, url_prefix='/writing',
    static_folder='static', template_folder='templates', )


@writing.route('/preamble')
def preamble():
    return render_template(
        'writing/preamble.html'
    )
