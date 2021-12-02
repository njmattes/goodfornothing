#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from flask import Blueprint
from flask import redirect, url_for


mod = Blueprint('main', __name__, static_folder='static')


@mod.route('/')
def index():
    return render_template(
        'index.html'
    )


@mod.route('/sketches')
def sketches():
    return render_template(
        'sketches.html'
    )


# REDIRECTS

@mod.route('/tunnelstacks')
def tunnelstacks():
    """Tunnelstacks was renamed pixilated. This redirects the old link."""
    return redirect(url_for('pixilated.index', code=302))
