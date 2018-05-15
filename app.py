#!/usr/bin/env python3
"""App for Zhai Ltd.
"""

import datetime as dt

from flask import Flask, request, abort, redirect, jsonify, make_response
from werkzeug import (
    generate_password_hash,
    check_password_hash,
    secure_filename,
)
from jinja2 import Environment, PackageLoader, select_autoescape
import jwt

import config
from model import *


def validate_form(*args):
    return all([s.isalnum() for s in args])


def validate_token(req):
    _, _, token = req.headers["Authorization"].partition("Bearer ")
    try:
        return jwt.decode(token, cfg["secret"])
    except:
        return False


def validate_filename(f):
    if len(f) > cfg["max_filename_length"]:
        return False
    _, _, ext = f.rpartition(".")
    return ext in cfg["allowed_fileexts"]


cfg = config.read()
students = Students(
    {
        "username": "1",
        "password": generate_password_hash("1"),
        "is_admin": True,
        "name": "Marline",
        "address": "Shenzhen",
        "contact": "10085",
    }
)
bulletins = Bulletins(
    {
        "title": "毕业快乐",
        "content": "祝大家答辩顺利！",
        "username": "1",
        "date": dt.datetime.now().ctime(),
    }
)
photos = Photos(
    {
        "filename": "activity.jpg",
        "username": "1",
        "date": dt.datetime.now().ctime(),
    }
)

app = Flask(__name__)
env = Environment(
    loader=PackageLoader(__name__, "templates"), autoescape=select_autoescape
)

[index_tmpl, app_tmpl, home_content_tmpl, user_content_tmpl] = [
    env.get_template(f)
    for f in ["index.html", "app.html", "home.html", "user.html"]
]


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
        assert check_password_hash(students[username]["password"], password)
        token = jwt.encode(
            {
                "username": username,
                "exp": dt.datetime.utcnow() + cfg["timedelta"],
            },
            cfg["secret"],
        )
        return jsonify({"token": token.decode("utf-8")})
    except:
        return make_response(jsonify({}), 401)


@app.route("/signup", methods=["POST"])
def signup():
    form = request.form
    try:
        username = form["username"]
        password = form["password"]
        assert validate_form(username, password)
        students[username] = {
            "username": username, "password": generate_password_hash(password)
        }
    except:
        return abort(400)
    else:
        return redirect("/")


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return app_tmpl.render(url="/home", username=user)
    else:
        try:
            assert validate_token(request)
            return home_content_tmpl.render(
                bulletins=bulletins.getall(students)
            )
        except Exception as e:
            raise e
            return abort(401)


@app.route("/user/<user>", methods=["GET", "POST"])
def user(user):
    if request.method == "GET":
        return app_tmpl.render(url="/user/{}".format(user), username=user)
    else:
        try:
            assert validate_token(request)
            return user_content_tmpl.render(username=user)
        except:
            return abort(401)


app.run()
