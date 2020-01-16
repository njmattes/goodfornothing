#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from flask import Blueprint


mod = Blueprint('main', __name__, static_folder='static')


@mod.route('/')
def index():
    return render_template(
        'index.html'
    )
