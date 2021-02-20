# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, url_for, session
from flask_session import Session
from flask_login import LoginManager
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path

login_manager = LoginManager()

def register_extensions(app):
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    register_extensions(app)
    register_blueprints(app)
    sess = Session()
    sess.init_app(app)
    return app
