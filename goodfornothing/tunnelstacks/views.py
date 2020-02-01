#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request


tunnelstacks = Blueprint(
    'tunnelstacks', __name__, url_prefix='/tunnelstacks',
    static_folder='static', template_folder='templates', )


@tunnelstacks.route('/')
def index():
    return render_template(
        'tunnelstacks/index.html',
        size=request.args.get('size') or 20,
        sides=request.args.get('sides') or 4,
        fg=request.args.get('user') or '0, 0, 0',
        bg=request.args.get('bg') or '255, 255, 255',
        opacity=request.args.get('opacity') or .05,
        time=request.args.get('time') or 300,
    )
