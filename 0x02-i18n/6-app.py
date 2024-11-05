#!/usr/bin/env python3
"""6-app.py"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Config"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.before_request
def before_request() -> None:
    """before request"""
    setattr(g,
            'user',
            users.get(int(request.args.get('login_as', 0)), 0))


@babel.localeselector
def get_locale() -> str:
    """get_locale"""
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    locale = g.user.get('locale', None) if g.user else None
    if locale and locale in Config.LANGUAGES:
        return locale
    locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if locale and locale in Config.LANGUAGES:
        return locale
    return Config.BABEL_DEFAULT_LOCALE


@app.route('/', strict_slashes=False)
def index() -> str:
    """ndex"""
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run()
