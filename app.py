#!/usr/bin/env python
"""App for Zhai Ltd.
"""

from flask import Flask, request
from werkzeug import generate_password_hash, check_password_hash
from jinja2 import Environment, PackageLoader, select_autoescape

app = Flask(__name__)
env = Environment(
    loader=PackageLoader(__name__, 'templates'), autoescape=select_autoescape
)
index_tmpl = env.get_template('index.html')


@app.route('/')
def homepage():
    return index_tmpl.render()


@app.route('/signin', methods=['POST'])
def signin():
    return 'signin'


@app.route('/signup', methods=['POST'])
def signup():
    return 'signup'


app.run()
