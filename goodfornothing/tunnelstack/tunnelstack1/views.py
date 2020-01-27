#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('tunnelstack1', __name__,
                url_prefix='/tunnelstack1',
                static_folder='static',
                )


@mod.route('/')
def index():
    return render_template(
        'images/tunnelstack/tunnelstack1.html',
        size=20,
        sides=4,
    )
