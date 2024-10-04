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

def check_login(username, password):
    if 6 <= len(username) <= 20:
        if 8 <= len(password) <= 64:
            return True
        
    return False

@app.route("/")
def index():
    login_ok = session.get("login_ok", True)

    # Reset session values
    session["login_ok"] = True

    return render_template("index.html", login_ok=login_ok) 

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["login_ok"] = False

    # check username and password
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["role"] = user.role
            session["login_ok"] = True
            return redirect(url_for("frontpage"))

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/create_user")
def create_user():
    length_ok = session.get("length_ok", True)
    username_ok = session.get("username_ok", True)
    password_ok = session.get("password_ok", True)
    user_added = session.get("user_added", False)

    # Reset session values
    session["length_ok"] = True
    session["username_ok"] = True
    session["password_ok"] = True
    session["user_added"] = False

    return render_template("create_user.html",
                           length_ok=length_ok,
                           username_ok=username_ok,
                           password_ok=password_ok,
                           user_added=user_added)

@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    session["length_ok"] = False

    # check the length of login credentials
    if check_login(username, password1):
        session["length_ok"] = True
        session["username_ok"] = False
        # check if user already exists
        sql = "SELECT COUNT(*) FROM users WHERE username = :username"
        c = db.session.execute(text(sql), {"username":username}).fetchone()[0]
        print(c)
        if c == 0:
            session["username_ok"] = True
            session["password_ok"] = False
            # check password and add user into database
            if password1 == password2:
                hash_value = generate_password_hash(password1)
                sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
                db.session.execute(text(sql), {"username":username, "password":hash_value})
                db.session.commit()
                session["password_ok"] = True
                session["user_added"] = True

    return redirect(url_for("create_user"))

@app.route("/frontpage")
def frontpage():
    return render_template("frontpage.html")

@app.route("/create_animal")
def create_animal():
    animal_added = session.get("animal_added", False)

    # Reset session values
    session["animal_added"] = False

    return render_template("create_animal.html", animal_added=animal_added)

@app.route("/add_animal", methods=["POST"])
def add_animal():
    # TBA: check input
    name = request.form["name"]
    species = request.form["species"]

    # TBA: add animal into database
    # TBA: check if animal already exists

    return redirect(url_for("create_animal"))

@app.route("/create_staff")
def create_staff():
    staff_added = session.get("staff_added", False)

    # Reset session values
    session["staff_added"] = False

    return render_template("create_staff.html", staff_added=staff_added)

@app.route("/add_staff", methods=["POST"])
def add_staff():
    name = request.form["name"]
    role = request.form["role"]
    date = request.form["date"]
    contact = request.form["contact"]

    # add staff member into database (existing name is allowed)
    sql = "INSERT INTO staff (name, role, hire_date, contact_info) VALUES (:name, :role, :date, :contact)"
    db.session.execute(text(sql), {"name":name, "role":role, "date":date, "contact":contact})
    db.session.commit()
    session["staff_added"] = True

    return redirect(url_for("create_staff"))

