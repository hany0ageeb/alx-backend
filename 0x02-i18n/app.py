#!/usr/bin/env python3
"""7-app.py"""
import pytz
import datetime
from flask import Flask, render_template, request, g
from flask_babel import Babel
from flask_babel import format_datetime
from typing import Union, Dict


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
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """tmezone"""
    tz = request.args.get('timezone', '').strip()
    if not tz and g.user:
        tz = g.user['timezone']
    try:
        return pytz.timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id: str) -> Union[Dict[str, Union[str, None]], None]:
    """get_user
    """
    return users.get(int(id), 0)


@app.before_request
def before_request() -> None:
    """before request"""
    setattr(g, 'user', get_user(request.args.get('login_as', 0)))
    setattr(g, 'time', format_datetime(datetime.datetime.now()))


@app.route('/', strict_slashes=False)
def index() -> str:
    """index"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
