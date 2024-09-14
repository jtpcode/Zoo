from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

# Show "wrong user/password" -notification or not
fresh_start = True

@app.route("/")
def index():
    return render_template("index.html", fresh_start=fresh_start) 

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

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
            fresh_start = True
            
    if "username" not in session:
        fresh_start = False

    return render_template("index.html", fresh_start=fresh_start)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")