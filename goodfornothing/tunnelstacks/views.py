#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request


mod = Blueprint('tunnelstacks', __name__,
                url_prefix='/tunnelstacks',
                static_folder='static',
                template_folder='templates',
                )


@mod.route('/')
def index():
    return render_template(
        'tunnelstacks/index.html',
        size=request.args.get('size') or 20,
        sides=request.args.get('sides') or 4,
        fg=request.args.get('user') or 'rgba(0, 0, 0, .01)',
        bg=request.args.get('bg') or 'rgba(255, 255, 255)',
    )
