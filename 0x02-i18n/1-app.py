#!/usr/bin/env python3
# 1-app.py
"""1-app.py
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Config
    """
    LANGUAGES = ["en", "fr"]


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)
# babel.init_app(app,
#               locale_selector=get_local,
#               timezone_selector=get_timezone)


@babel.localeselector
def get_locale():
    """get_locale"""
    return Config.LANGUAGES[0]


@babel.timezoneselector
def get_timezone():
    """get_tmezone"""
    return "UTC"


@app.route("/")
def index():
    """index
    """
    return render_template('1-index.html')
