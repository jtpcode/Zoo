from sqlalchemy.sql import text
from db import db

def get_user(username):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    return db.session.execute(text(sql), {"username":username})

def user_exists(username):
    sql = "SELECT COUNT(*) FROM users WHERE username = :username"
    return db.session.execute(text(sql), {"username":username}).fetchone()[0]

def add_user(username, hash_value):
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()

def get_species():
    sql = "SELECT id, species FROM species;"
    return db.session.execute(text(sql)).fetchall()

def get_origin():
    sql = "SELECT id, origin FROM origin;"
    return db.session.execute(text(sql)).fetchall()

def get_diagnoses():
    sql = "SELECT id, diagnosis FROM diagnosis;"
    return db.session.execute(text(sql)).fetchall()

def get_staff(role):
    sql = "SELECT id, name FROM staff WHERE role = :role;"
    return db.session.execute(text(sql), {"role":role}).fetchall()

def animal_exists(name):
    sql = "SELECT COUNT(*) FROM animal WHERE name = :name"
    return db.session.execute(text(sql), {"name":name}).fetchone()[0]

def add_animal(name, species_id, gender, birthday, origin_id, diet, staff_id):
    sql = """INSERT INTO animal (name, species_id, gender, birthday, origin_id, diet, staff_id)
             VALUES (:name, :species_id, :gender, :birthday, :origin_id, :diet, :staff_id)
             RETURNING id"""
    id = db.session.execute(text(sql),
            {"name":name, "species_id":species_id, "gender":gender, "birthday":birthday,
             "origin_id":origin_id, "diet":diet, "staff_id":staff_id})
    db.session.commit()
    return id

def add_diagnoses(animal_id, id):
    sql = """INSERT INTO animal_diagnosis (animal_id, diagnosis_id)
             VALUES (:animal_id, :diagnosis_id)"""
    db.session.execute(text(sql), {"animal_id":animal_id, "diagnosis_id":id})
    db.session.commit()

def add_staff(name, role, date, contact):
    sql = """INSERT INTO staff (name, role, hire_date, contact_info)
             VALUES (:name, :role, :date, :contact)"""
    db.session.execute(text(sql), {"name":name, "role":role, "date":date, "contact":contact})
    db.session.commit()

def get_animal_info(name):
    sql = """SELECT a.id, a.name, s.species, a.gender, a.birthday, o.origin, a.diet,
             st.name, a.deceased
             FROM animal a
             LEFT JOIN species s ON a.species_id = s.id
             LEFT JOIN origin o ON a.origin_id = o.id
             LEFT JOIN staff st ON a.staff_id = st.id
             WHERE a.name = :name"""
    return db.session.execute(text(sql), {"name":name}).fetchone()

def get_animal_diagnoses(name):
    sql = """SELECT COALESCE(string_agg(d.diagnosis, ', '), '-') AS diagnoses
             FROM diagnosis d
             LEFT JOIN animal_diagnosis ad ON d.id = ad.diagnosis_id
             LEFT JOIN animal a ON ad.animal_id = a.id
             WHERE a.name = :name"""
    return db.session.execute(text(sql), {"name":name}).fetchone()

def get_animal_records(name):
    sql = """SELECT mr.date, u.username, mr.record
             FROM medical_record mr
             LEFT JOIN animal a ON mr.animal_id = a.id
             LEFT JOIN users u ON mr.user_id = u.id 
             WHERE a.name = :name"""
    return db.session.execute(text(sql), {"name":name}).fetchall()

def add_record(record, animal_id, user_id):
    sql = """INSERT INTO medical_record (record, animal_id, user_id)
             VALUES (:record, :animal_id, :user_id)"""
    db.session.execute(text(sql), {"record":record, "animal_id":animal_id,
                                   "user_id":user_id})
    db.session.commit()
