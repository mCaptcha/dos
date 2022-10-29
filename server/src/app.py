# TODO demo
# Copyright © 2021 Aravinth Manivannan <realaravinth@batsense.net
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
import os
import string
import random

from flask import (
    Flask,
    render_template,
    session,
    request,
    redirect,
    url_for,
    make_response,
    send_from_directory,
)
import sqlite3
from flask_bcrypt import Bcrypt
from flask import g
import requests


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


DATABASE = "databse.db"
app = Flask(__name__)
app.secret_key = bytes(
    "".join(random.choices(string.ascii_uppercase + string.digits, k=40)), "utf-8"
)
app.logger.setLevel(logging.DEBUG)
bcrypt = Bcrypt(app)
init_db()

mcaptcha_secret = os.getenv("MCAPTCHA_SECRET")
mcaptcha_sitekey = os.getenv("MCAPTCHA_SITEKEY")


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("list.html")


@app.route("/unprotected", methods=["POST", "GET"])
def unprotected():
    error = None
    if request.method == "POST":
        username = str.strip(request.form["username"])
        password = str.strip(request.form["password"])
        confirm_password = str.strip(request.form["confirm_password"])

        if confirm_password != password:
            error = "Passwords don't match"
            return render_template("index.html")

        register(username, password)
        return render_template("index.html")
    else:
        return render_template("unprotected.html", error=error)


@app.route("/protected", methods=["POST", "GET"])
def protected():
    error = None
    if request.method == "POST":
        username = str.strip(request.form["username"])
        password = str.strip(request.form["password"])
        confirm_password = str.strip(request.form["confirm_password"])

        if confirm_password != password:
            error = "Passwords don't match"
            print(error)
            return "passwords don't match", 400

        mcaptcha_token = str.strip(request.form["mcaptcha__token"])

        payload = {
            "token": mcaptcha_token,
            "key": mcaptcha_sitekey,
            "secret": mcaptcha_secret,
        }
        resp = requests.post(
            "http://localhost:7000/api/v1/pow/siteverify", json=payload
        )
        resp = resp.json()
        if resp["error"]:
            return resp["error"], 500
        elif resp["valid"] == False:
            return "invalid captcha", 400
        else:
            register(username, password)
            return render_template("index.html")
    else:
        return render_template("protected.html", sitekey=mcaptcha_sitekey)


def register(username: str, password: str):
    stored_hash = bcrypt.generate_password_hash(password, rounds=12)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO todo_users (name, hash) VALUES (?, ?);", (username, stored_hash)
    )
    conn.commit()
    conn.close()


@app.teardown_appcontext
def close_connection(_exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
