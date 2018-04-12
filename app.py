#!/usr/bin/env python
"""App for Zhai Ltd.
"""

from flask import Flask, request, abort, redirect
from werkzeug import generate_password_hash, check_password_hash
from jinja2 import Environment, PackageLoader, select_autoescape

from models import *

app = Flask(__name__)
env = Environment(
    loader=PackageLoader(__name__, 'templates'), autoescape=select_autoescape
)
index_tmpl = env.get_template('index.html')
dogs = Dogs()


@app.route('/')
def homepage():
    return index_tmpl.render()


@app.route('/signin', methods=['POST'])
def signin():
    form = request.form
    try:
        assert check_password_hash(dogs[form['username']], form['password'])
    except:
        abort(401)
    return 'Hi, {}!'.format(form['username'])


@app.route('/signup', methods=['POST'])
def signup():
    try:
        dogs[request.form['username']] = generate_password_hash(
            request.form['password']
        )
    except:
        abort(400)
    return redirect('/')


app.run()
