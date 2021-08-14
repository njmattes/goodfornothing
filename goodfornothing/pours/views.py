#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod = Blueprint('pours', __name__,
                url_prefix='/pours',
                static_folder='static',
                template_folder='templates',
                )


@mod.route('/')
def index():
    return render_template(
        'pours/index.html',
    )
