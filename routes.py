from app import app
from flask import redirect, render_template, request, session, url_for, abort
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
import secrets
import sql

app.secret_key = getenv("SECRET_KEY")

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
    result = sql.get_user(username)
    user = result.fetchone()
    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            session["role"] = user.role
            session["login_ok"] = True
            session["logged_in"] = True
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(url_for("frontpage"))

    return redirect(url_for("index"))

@app.route("/frontpage")
def frontpage():
    if "logged_in" not in session:
        return redirect(url_for("index"))
    
    return render_template("frontpage.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/create_user")
def create_user():
    if "logged_in" not in session:
        return redirect(url_for("index"))
    
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
        c = sql.user_exists(username)
        if c == 0:
            session["username_ok"] = True
            session["password_ok"] = False
            # Check password and add user into database
            if password1 == password2:
                hash_value = generate_password_hash(password1)
                session["password_ok"] = True
                try:
                    sql.add_user(username, hash_value)
                    session["user_added"] = True
                except Exception as e:
                    print(f"Error: {e}")
                    session["sql_error"] = True

    return redirect(url_for("create_user"))

@app.route("/create_staff")
def create_staff():
    if "logged_in" not in session:
        return redirect(url_for("index"))
    
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

    # Add staff member into database (existing name is allowed)
    try:
        sql.add_staff(name, role, date, contact)
        session["staff_added"] = True
    except Exception as e:
            print(f"Error: {e}")
            session["sql_error"] = True

    return redirect(url_for("create_staff"))

@app.route("/create_animal")
def create_animal():
    if "logged_in" not in session:
        return redirect(url_for("index"))
    
    animal_added = session.get("animal_added", False)
    name_ok = session.get("name_ok", True)
    sql_error = session.get("sql_error", False)

    # Reset session values
    session["animal_added"] = False
    session["name_ok"] = True
    session["sql_error"] = False

    # Data for drop down menus
    species_list = sql.get_species()
    origin_list = sql.get_origin()
    diagnosis_list = sql.get_diagnoses()
    staff = sql.get_staff("Hoitaja")

    return render_template("create_animal.html",
                           animal_added=animal_added,
                           species_list=species_list,
                           origin_list=origin_list,
                           diagnosis_list=diagnosis_list,
                           staff=staff,
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
    staff_id = request.form["staff"]

    # Check if animal name already exists
    c = sql.animal_exists(name)
    if c == 0:
        try:
            # Add animal into database
            result = sql.add_animal(name, species_id, gender, birthday, origin_id, diet, staff_id)
            animal_id = result.fetchone()[0]

            # Chosen diagnoses into junction table
            if diagnoses:
                for id in diagnoses:
                    sql.add_diagnoses(animal_id, id)
            session["animal_added"] = True
        except Exception as e:
            print(f"Error: {e}")
            session["sql_error"] = True
    else:
        session["name_ok"] = False

    return redirect(url_for("create_animal"))

@app.route("/animal_records")
def animal_records():
    if "logged_in" not in session:
        return redirect(url_for("index"))
    
    animal_found = session.get("animal_found", True)
    animal_data = None
    diagnoses = None
    records = None

    # Reset session values
    session["animal_found"] = True

    # If animal with correct name has been searched, get animal data
    if "animal_name" in session:
        # Get animal basic information and medical records
        name = session["animal_name"]
        animal_data = sql.get_animal_info(name)      
        diagnoses = sql.get_animal_diagnoses(name)
        records = sql.get_animal_records(name)

        # Store animal_id for creating new medical records
        session["animal_id"] = animal_data[0]

    return render_template("animal_records.html",
                           animal_found=animal_found,
                           animal_data=animal_data,
                           diagnoses = diagnoses,
                           records=records)

@app.route("/search_animal", methods=["POST"])
def search_animal():
    # csrf check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    # Check if animal in database
    name = request.form["name"]
    c = sql.animal_exists(name)
    if c != 0:
        session["animal_name"] = name
    else:
        session["animal_found"] = False
    
    return redirect(url_for("animal_records"))

@app.route("/create_record", methods=["GET", "POST"])
def create_record():
    if "logged_in" not in session:
        return redirect(url_for("index"))
    
    sql_error = session.get("sql_error", False)

    # Reset session values
    session["sql_error"] = False

    if request.method == "POST":
        # csrf check
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        # Add medical record into database
        record = request.form["record"]
        try:
            sql.add_record(record, session["animal_id"], session["user_id"])
            return redirect(url_for("animal_records"))
        except Exception as e:
            print(f"Error: {e}")
            session["sql_error"] = True

            return redirect(url_for("create_record"))

    return render_template("create_record.html",
                           sql_error=sql_error)

