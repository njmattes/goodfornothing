#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_assets import Environment, Bundle
from flask_session import Session
from goodfornothing.no1.views import mod as no1_views
from goodfornothing.selfie1.views import selfie1
from goodfornothing.walldrawings.views import walldrawing
from goodfornothing.tunnelstacks.views import tunnelstacks
from goodfornothing.hal9000portrait.views import mod as hal9000_views
from goodfornothing.views import mod as main_views


app = Flask(__name__)
app.config.from_object('goodfornothing.config.FlaskConfig')
Session(app)

app.register_blueprint(main_views)
app.register_blueprint(no1_views)
app.register_blueprint(selfie1)
app.register_blueprint(walldrawing)
app.register_blueprint(tunnelstacks)
app.register_blueprint(hal9000_views)

print(app.url_map)

assets = Environment(app)
assets.register('img_favicon',
                Bundle('images/favicon.png', output='gen/favicon.png'))
