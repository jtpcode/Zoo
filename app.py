from flask import Flask
from flask import redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    login_ok_str = request.args.get("login_ok", default="True")
    # Change str -> bool
    login_ok = login_ok_str == "True"

    return render_template("index.html", login_ok=login_ok) 

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    login_ok = False

    # check username and password
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone() 
    if user:
        # correct username 
        hash_value = user.password
        if check_password_hash(hash_value, password):
            # correct password
            session["username"] = username
            login_ok = True

    return redirect(url_for("index", login_ok=login_ok))

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_user")
def create_user():
    password_ok_str = request.args.get("password_ok", default="True")
    # Change str -> bool
    password_ok = password_ok_str == "True"

    return render_template("create_user.html", password_ok=password_ok)

@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    # check password
    if password1 == password2:
        hash_value = generate_password_hash(password1)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()

        return redirect(url_for("user_added"))
    else:
        password_ok = False
        return redirect(url_for("create_user", password_ok=password_ok))

@app.route("/user_added")
def user_added():
    return "<p>Käyttäjätunnus luotu onnistuneesti!</p><a href='/'>Siirry kirjautumissivulle</a>"

