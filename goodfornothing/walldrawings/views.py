#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


walldrawing = Blueprint(
    'walldrawings', __name__, url_prefix='/walldrawing',
    static_folder='static', template_folder='templates', )


@walldrawing.route('/no1')
def walldrawing_no1():
    return render_template(
        'walldrawings/no1.html'
    )


@walldrawing.route('/6114a')
def walldrawing_6114a():
    return render_template(
        'walldrawings/6114a.html'
    )
