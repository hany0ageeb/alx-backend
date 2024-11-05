#!/usr/bin/env python3
# 3-app.py
"""3-app.py"""
from flask import Flask, request, render_template
from flask_babel import Babel


class Config:
    """Config"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """get_locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """index"""
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run()
