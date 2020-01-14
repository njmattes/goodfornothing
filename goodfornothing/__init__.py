#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_assets import Environment, Bundle
from flask_session import Session
from goodfornothing.no1.views import mod as no1_views
from goodfornothing.z2017a.views import mod as z2017a_views
from goodfornothing.z2017b.views import mod as z2017b_views


app = Flask(__name__)
app.config.from_object('goodfornothing.config.FlaskConfig')
Session(app)

app.register_blueprint(no1_views)
app.register_blueprint(z2017a_views)
app.register_blueprint(z2017b_views)

assets = Environment(app)
assets.register('img_favicon',
                Bundle('images/favicon.png', output='gen/favicon.png'))
