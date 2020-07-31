#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

writing = Blueprint(
    'writing', __name__, url_prefix='/writing',
    static_folder='static', template_folder='templates', )


@writing.route('/preamble')
def preamble():
    """Index page for abstract submitted to CICA

    :return: Template for abstract/preamble
    :rtype: str
    """
    return render_template(
        'writing/preamble.html'
    )


@writing.route('/bios')
def bios():
    """Bios

    :return: Template for bios
    :rtype: str
    """
    return render_template(
        'writing/bios.html'
    )
