#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_assets import Environment, Bundle
from flask_session import Session
from goodfornothing.no1.views import mod as no1_views
from goodfornothing.selfie1.views import mod as selfie1_views
from goodfornothing.walldrawing.walldrawing1.views import mod as walldrawing1_views
from goodfornothing.walldrawing.walldrawing6114a.views import mod as walldrawing6114a_views
from goodfornothing.hal9000portrait.views import mod as hal9000_views
from goodfornothing.views import mod as main_views


app = Flask(__name__)
app.config.from_object('goodfornothing.config.FlaskConfig')
Session(app)

app.register_blueprint(main_views)
app.register_blueprint(no1_views)
app.register_blueprint(selfie1_views)
app.register_blueprint(walldrawing1_views)
app.register_blueprint(walldrawing6114a_views)
app.register_blueprint(hal9000_views)

assets = Environment(app)
assets.register('img_favicon',
                Bundle('images/favicon.png', output='gen/favicon.png'))
