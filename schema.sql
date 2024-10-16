CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    registered TIMESTAMP(0) DEFAULT NOW()
);

CREATE TABLE species (
    id SERIAL PRIMARY KEY,
    species TEXT NOT NULL
);

CREATE TABLE origin (
    id SERIAL PRIMARY KEY,
    origin TEXT NOT NULL
);

CREATE TABLE staff (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    hire_date DATE NOT NULL,
    contact_info TEXT
);

CREATE TABLE diagnosis (
    id SERIAL PRIMARY KEY,
    diagnosis TEXT NOT NULL
);

CREATE TABLE animal (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    species_id INTEGER NOT NULL REFERENCES species,
    gender TEXT NOT NULL,
    birthday DATE NOT NULL,
    origin_id INTEGER NOT NULL REFERENCES origin,
    diet TEXT,
    staff_id INTEGER NOT NULL REFERENCES staff,
    deceased DATE DEFAULT NULL
);

CREATE TABLE animal_diagnosis (
    PRIMARY KEY (animal_id, diagnosis_id),
    animal_id INTEGER REFERENCES animal,
    diagnosis_id INTEGER REFERENCES diagnosis
);

CREATE TABLE medical_record (
    id SERIAL PRIMARY KEY,
    record TEXT NOT NULL,
    animal_id INTEGER NOT NULL REFERENCES animal,
    user_id INTEGER NOT NULL REFERENCES users,
    date TIMESTAMP(0) DEFAULT NOW()
);

