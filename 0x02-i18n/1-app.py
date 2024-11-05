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
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'


@app.route("/")
def index():
    """index
    """
    return render_template('1-index.html')
