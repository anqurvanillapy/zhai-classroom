#!/usr/bin/env python3
"""App for Zhai Ltd.
"""

import datetime as dt

from flask import Flask, request, abort, redirect, jsonify
from werkzeug import generate_password_hash, check_password_hash
from jinja2 import Environment, PackageLoader, select_autoescape
import jwt

import config
from util import *

cfg = config.read()
dogs = Dogs()

app = Flask(__name__)
env = Environment(
    loader=PackageLoader(__name__, "templates"), autoescape=select_autoescape
)
index_tmpl = env.get_template("index.html")


@app.route("/")
def homepage():
    return index_tmpl.render()


@app.route("/signin", methods=["POST"])
def signin():
    form = request.form
    try:
        username = form["username"]
        password = form["password"]
        assert validate_form(username, password)
        assert check_password_hash(dogs[username], password)
        token = jwt.encode(
            {"exp": dt.datetime.utcnow() + cfg["timedelta"]}, cfg["secret"]
        )
        return jsonify({"token": token.decode("utf-8")})
    except Exception as e:
        # raise e
        return abort(401)


@app.route("/signup", methods=["POST"])
def signup():
    form = request.form
    try:
        username = form["username"]
        password = form["password"]
        assert validate_form(username, password)
        dogs[username] = generate_password_hash(password)
    except:
        abort(400)
    return redirect("/")


@app.route("/user/<user>/")
def user(user):
    return "<p>Hello, {}</p>".format(user)


app.run()
