#!/usr/bin/env python3
"""App for Zhai Ltd.
"""

import datetime as dt

from flask import Flask, request, abort, redirect, jsonify, make_response
from werkzeug import generate_password_hash, check_password_hash
from jinja2 import Environment, PackageLoader, select_autoescape
import jwt

import config
from model import *


def validate_form(*args):
    # 验证表单的正确性, 即:
    # 1. args 是一个 list, 里面的所有元素都将是 string.
    # 2. [s.isalnum() for s in args], 创建一个新的 list, list 的每一个元素都是
    # bool 类型, 它判断 args 中每一个字符串是不是 alphanumeric 的, 即字符串仅由
    # *数字和字母* 组成, 不能有空格或标点符号等.
    # 3. all([s.isalnum() for s in args]) 每一个字符串都必须是 alphanumeric 的.
    return all([s.isalnum() for s in args])


def validate_token(req):
    _, _, token = req.headers["Authorization"].partition("Bearer ")
    try:
        return jwt.decode(token, cfg["secret"])
    except:
        return False


# 获得 app 的配置, 类型是 dict.
cfg = config.read()
# 创建一个存放 Dogs 的数据库实例.  提前创建一个狗子叫 a, 密码为 a, 方便我们测试.
dogs = Dogs({"a": generate_password_hash("a")})

# 创建一个 Flask app 实例, 名字是模块的名字 (__name__).
app = Flask(__name__)
# 初始化 HTML 模板的环境, 并开启自动转义功能 (把不支持的字符进行转换).
env = Environment(
    loader=PackageLoader(__name__, "templates"), autoescape=select_autoescape
)

# 主页模板, 位置在 templates/index.html.
index_tmpl = env.get_template("index.html")
# 个人主页模板.
profile_tmpl = env.get_template("profile.html")


@app.route("/")
def homepage():
    return index_tmpl.render()


# 用户通过 POST 方法访问 /signin.
@app.route("/signin", methods=["POST"])
def signin():
    # 我们假定用户发来了一个表格, 从用户请求中获取这个表单.
    form = request.form
    try:
        username = form["username"]
        password = form["password"]
        # 断定用户名和密码是合法的, 详见其实现 (util.py 里), 否则抛出
        # AssertionError 异常.
        assert validate_form(username, password)
        # 从 dogs 中获得一个狗子, 狗子的密码和用户提交的密码是否一致.
        assert check_password_hash(dogs[username], password)
        # 生成令牌, 过期时间为一周, 秘密为一个用户定义的特殊字段.
        token = jwt.encode(
            {"exp": dt.datetime.utcnow() + cfg["timedelta"]}, cfg["secret"]
        )
        # 把这个令牌转正 JSON 格式返回给用户.
        return jsonify({"token": token.decode("utf-8")})
    except:
        # 发生异常情况, 返回 401 (用户无权限) 错误码给用户, 告诉用户无权登录.
        return make_response(jsonify({}), 401)


@app.route("/signup", methods=["POST"])
def signup():
    form = request.form
    try:
        username = form["username"]
        password = form["password"]
        assert validate_form(username, password)
        # 添加一个新的狗子, 为狗子生成密码.
        dogs[username] = generate_password_hash(password)
    except:
        # 如果发生错误, 返回 400 (无效请求) 给用户, 告诉用户操作不能进行.
        return abort(400)
    else:
        # 未发生错误, 让用户返回到首页, 以便登录.
        return redirect("/")


@app.route("/user/<user>/")
def user(user):
    try:
        assert validate_token(request)
        return profile_tmpl.render(username=user)
    except:
        return abort(401)


app.run()
