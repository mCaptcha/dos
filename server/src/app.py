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

from flask import Flask, render_template, session, request, redirect, url_for, make_response
import sqlite3
from flask_bcrypt import Bcrypt
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

DATABASE = 'databse.db'
app = Flask(__name__)
app.secret_key = bytes(''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 40)), "utf-8")
app.logger.setLevel(logging.DEBUG)
bcrypt = Bcrypt(app)
init_db()

@app.route("/", methods=["POST", "GET"])
def index():
    if 'username' in session:
        username = session["username"]
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route("/join", methods=["POST", "GET"])
def join():
    error = None
    if request.method == 'POST':
        username = str.strip(request.form['username'])
        password = str.strip(request.form['password'])
        confirm_password = str.strip(request.form['confirm_password'])

        if confirm_password != password:
            error = "Passwords don't match"
            return render_template('join.html', error=error)

        register(username, password)
        return redirect(url_for('login'))
    else:
        return render_template('join.html', error=error)

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_login(username, password):
            resp = make_response(redirect(url_for('index')))
            session['username'] = username
            return resp
        else:
            error = 'Invalid username/password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html', error=error)

def validate_login(username: str, password: str) -> bool:
    cur = get_db().cursor()
    stored_hash = cur.execute('SELECT hash FROM todo_users WHERE name = ?', [username]).fetchone()[0]
    return stored_hash is not None and bcrypt.check_password_hash(stored_hash, password)

def register(username: str, password: str):
    stored_hash = bcrypt.generate_password_hash(password, rounds=12)
    conn = get_db();
    cur = conn.cursor()
    cur.execute('INSERT INTO todo_users (name, hash) VALUES (?, ?);', (username, stored_hash))
    conn.commit()
    conn.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.teardown_appcontext
def close_connection(_exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
