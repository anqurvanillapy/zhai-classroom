#!/usr/bin/env python3
"""App for Zhai Ltd.
"""

import datetime as dt
import json
from os import path

from flask import (
    Flask,
    request,
    abort,
    redirect,
    jsonify,
    make_response,
    send_from_directory,
)
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
    },
    {
        "username": "2",
        "password": generate_password_hash("2"),
        "is_admin": False,
        "name": "Anqur",
        "address": "Shenzhen",
        "contact": "10086",
    },
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
        "filename": "grad.jpg",
        "username": "1",
        "date": dt.datetime.now().ctime(),
    }
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = cfg["max_content_length"]
env = Environment(
    loader=PackageLoader(__name__, "templates"), autoescape=select_autoescape
)

[index_tmpl, app_tmpl, user_content_tmpl, profile_content_tmpl] = [
    env.get_template(f)
    for f in ["index.html", "app.html", "user.html", "profile.html"]
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


@app.route("/user/<user>", methods=["GET", "POST"])
def user(user):
    if request.method == "GET":
        return app_tmpl.render(url="/user/{}".format(user), username=user)
    else:
        try:
            assert validate_token(request)
            return user_content_tmpl.render(
                username=user,
                is_admin=students[user]["is_admin"],
                students=students.getall(),
                bulletins=enumerate(bulletins.getall()),
                photos=enumerate(photos.getall()),
            )
        except Exception as e:
            raise e
            return abort(401)


@app.route("/profile/<user>", methods=["GET", "POST"])
def profile(user):
    if request.method == "GET":
        return app_tmpl.render(url="/profile/{}".format(user), username=user)
    else:
        try:
            assert validate_token(request)
            return profile_content_tmpl.render(**students[user])
        except:
            return abort(401)


@app.route("/set/student", methods=["POST"])
def admin_set_student():
    try:
        form = request.form.to_dict()
        form["is_admin"] = students[form["username"]]["is_admin"]
        form["password"] = generate_password_hash(form["password"])
        students[request.form["username"]] = form
        return redirect("/user/{}".format(request.form["uploader"]))
    except Exception as e:
        raise
        return abort(400)


@app.route("/del/student", methods=["POST"])
def admin_del_student():
    try:
        del students[request.form["username"]]
        return redirect("/user/{}".format(request.form["admin"]))
    except:
        return abort(400)


@app.route("/add/bulletin", methods=["POST"])
def admin_set_bulletin():
    try:
        assert validate_form(request.form["title"], request.form["content"])
        form = request.form.to_dict()
        form["date"] = dt.datetime.now().ctime()
        bulletins.setitem(form)
        return redirect("/user/{}".format(request.form["username"]))
    except:
        return abort(400)


@app.route("/del/bulletin", methods=["POST"])
def admin_del_bulletin():
    try:
        bulletins.delitem(int(request.form["index"]))
        return redirect("/user/{}".format(request.form["username"]))
    except Exception as e:
        raise e
        return abort(400)


@app.route("/add/photo", methods=["POST"])
def admin_set_photo():
    try:
        f = request.files["file"]
        assert validate_filename(f.filename)
        filepath = secure_filename(f.filename)
        f.save(path.join(cfg["img_path"], filepath))
        photos.setitem(
            {"filename": f.filename, "date": dt.datetime.now().ctime()}
        )
        return redirect("/user/{}".format(request.form["username"]))
    except Exception as e:
        raise e
        return abort(400)


@app.route("/del/photo", methods=["POST"])
def admin_del_photo():
    try:
        photos.delitem(int(request.form["index"]))
        return redirect("/user/{}".format(request.form["username"]))
    except:
        return abort(400)


@app.route("/img/<path:f>")
def send_img(f):
    return send_from_directory(cfg["img_path"], f)


app.run()
