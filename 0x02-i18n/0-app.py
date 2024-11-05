#!/usr/bin/env python3
# 0-app.py
"""0-app.py
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """index
    """
    return render_template('0-index.html')
