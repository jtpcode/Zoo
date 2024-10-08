from flask import Flask
from flask import redirect, render_template, request, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

### NOTES: ###

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

    # Check username and password
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["role"] = user.role
            session["login_ok"] = True
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(url_for("frontpage"))

    return redirect(url_for("index"))

@app.route("/frontpage")
def frontpage():
    return render_template("frontpage.html")

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
    sql_error = session.get("sql_error", False)

    # Reset session values
    session["length_ok"] = True
    session["username_ok"] = True
    session["password_ok"] = True
    session["user_added"] = False
    session["sql_error"] = False

    return render_template("create_user.html",
                           length_ok=length_ok,
                           username_ok=username_ok,
                           password_ok=password_ok,
                           user_added=user_added,
                           sql_error=sql_error)

@app.route("/add_user", methods=["POST"])
def add_user():
    # csrf check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    session["length_ok"] = False

    # Check the length of login credentials
    if check_login(username, password1):
        session["length_ok"] = True
        session["username_ok"] = False
        # Check if user already exists
        sql = "SELECT COUNT(*) FROM users WHERE username = :username"
        c = db.session.execute(text(sql), {"username":username}).fetchone()[0]
        if c == 0:
            session["username_ok"] = True
            session["password_ok"] = False
            # Check password and add user into database
            if password1 == password2:
                hash_value = generate_password_hash(password1)
                session["password_ok"] = True
                try:
                    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
                    db.session.execute(text(sql), {"username":username, "password":hash_value})
                    db.session.commit()
                    session["user_added"] = True
                except Exception as e:
                    print(f"Error: {e}")
                    session["sql_error"] = True

    return redirect(url_for("create_user"))

@app.route("/create_animal")
def create_animal():
    animal_added = session.get("animal_added", False)
    name_ok = session.get("name_ok", True)
    sql_error = session.get("sql_error", False)

    # Reset session values
    session["animal_added"] = False
    session["name_ok"] = True
    session["sql_error"] = False

    # Data for drop down menus
    role = "Hoitaja"
    sql = "SELECT id, species FROM species;"
    species_list = db.session.execute(text(sql)).fetchall()
    sql = "SELECT id, origin FROM origin;"
    origin_list = db.session.execute(text(sql)).fetchall()
    sql = "SELECT id, diagnosis FROM diagnosis;"
    diagnosis_list = db.session.execute(text(sql)).fetchall()
    sql = "SELECT id, name FROM staff WHERE role = :role;"
    caretaker_list = db.session.execute(text(sql), {"role":role}).fetchall()

    return render_template("create_animal.html",
                           animal_added=animal_added,
                           species_list=species_list,
                           origin_list=origin_list,
                           diagnosis_list=diagnosis_list,
                           caretaker_list=caretaker_list,
                           name_ok=name_ok,
                           sql_error=sql_error)

@app.route("/add_animal", methods=["POST"])
def add_animal():
    # csrf check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    name = request.form["name"]
    species_id = request.form["species"]
    gender = request.form["gender"]
    birthday = request.form["birthday"]
    origin_id = request.form["origin"]
    diet = request.form["diet"]
    diagnoses = request.form.getlist("diagnosis")
    caretaker_id = request.form["caretaker"]

    # Check if animal name already exists
    sql = "SELECT COUNT(*) FROM animal WHERE name = :name"
    c = db.session.execute(text(sql), {"name":name}).fetchone()[0]
    if c == 0:
        try:
            # Animal into database
            sql = "INSERT INTO animal (name, species_id, gender, birthday, origin_id, diet, caretaker_id)" \
                "VALUES (:name, :species_id, :gender, :birthday, :origin_id, :diet, :caretaker_id) RETURNING id"
            result = db.session.execute(text(sql),
                    {"name":name, "species_id":species_id, "gender":gender, "birthday":birthday, "origin_id":origin_id,
                    "diet":diet, "caretaker_id":caretaker_id})
            animal_id = result.fetchone()[0]

            # Chosen diagnoses into junction table
            if diagnoses:
                for id in diagnoses:
                    sql = "INSERT INTO animal_diagnosis (animal_id, diagnosis_id) VALUES (:animal_id, :diagnosis_id)"
                    db.session.execute(text(sql), {"animal_id":animal_id, "diagnosis_id":id})

            db.session.commit()
            session["animal_added"] = True
        except Exception as e:
            print(f"Error: {e}")
            session["sql_error"] = True
    else:
        session["name_ok"] = False

    return redirect(url_for("create_animal"))

@app.route("/create_staff")
def create_staff():
    staff_added = session.get("staff_added", False)
    sql_error = session.get("sql_error", False)

    # Reset session values
    session["staff_added"] = False
    session["sql_error"] = False

    return render_template("create_staff.html",
                           staff_added=staff_added,
                           sql_error=sql_error)

@app.route("/add_staff", methods=["POST"])
def add_staff():
    # csrf check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    name = request.form["name"]
    role = request.form["role"]
    date = request.form["date"]
    contact = request.form["contact"]

    # Staff member into database (existing name is allowed)
    try:
        sql = "INSERT INTO staff (name, role, hire_date, contact_info) VALUES (:name, :role, :date, :contact)"
        db.session.execute(text(sql), {"name":name, "role":role, "date":date, "contact":contact})
        db.session.commit()
        session["staff_added"] = True
    except Exception as e:
            print(f"Error: {e}")
            session["sql_error"] = True

    return redirect(url_for("create_staff"))

@app.route("/animal_records")
def animal_records():
    animal_found = session.get("animal_found", True)
    animal_data = None
    diagnoses = None

    # Reset session values
    session["animal_found"] = True

    try:
        if session["animal_name"]:
            sql = """SELECT a.name, s.species, a.gender, a.birthday, o.origin, a.diet, st.name, a.deceased
                    FROM animal a
                    LEFT JOIN species s ON a.species_id = s.id
                    LEFT JOIN origin o ON a.origin_id = o.id
                    LEFT JOIN staff st ON a.caretaker_id = st.id
                    WHERE a.name = :name"""
            animal_data = db.session.execute(text(sql), {"name":session["animal_name"]}).fetchall()
            sql = """SELECT COALESCE(string_agg(d.diagnosis, ', '), '-') AS diagnoses
                    FROM diagnosis d
                    LEFT JOIN animal_diagnosis ad ON d.id = ad.diagnosis_id
                    LEFT JOIN animal a ON ad.animal_id = a.id
                    WHERE a.name = :name"""
            diagnoses = db.session.execute(text(sql), {"name":session["animal_name"]}).fetchall()
    except:
        pass

    return render_template("animal_records.html",
                           animal_found=animal_found,
                           animal_data=animal_data,
                           diagnoses = diagnoses)

@app.route("/search_animal", methods=["POST"])
def search_animal():
    # csrf check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    # Check if animal in database
    sql = "SELECT 1 FROM animal WHERE name = :name"
    found = db.session.execute(text(sql), {"name":name}).fetchone()
    if found:
        session["animal_name"] = name
    else:
        session["animal_found"] = False
    
    return redirect(url_for("animal_records"))