INSERT INTO users (username, password, role)
VALUES (
    'admin',
    'scrypt:32768:8:1$GFUKCZNDlSBdP4en$5c7b143831d859c687cfee818f6eb15bd806b2d1e82aaa76c981fb6a7f763b508a8f019e5a05584274d3f8aa2faa8ef051928d887cc5c94de044094be7e002e9',
    'admin'
);

INSERT INTO users (username, password, role)
VALUES (
    'Hanna Hoituri',
    'scrypt:32768:8:1$SxXmxhhajmghM8ux$9c8217eab8120b69a97ef376932c63c653ee2a2b1d2821c45c61707eda071b59efeb61219f171143f3f0eeb98583b999d945425517415233509391620cda7b0a',
    'user'
);

INSERT INTO users (username, password, role)
VALUES (
    'Kalle Kalamies',
    'scrypt:32768:8:1$v8pufQxleC1BCpmt$ee9ffca26c3de976b99d35d029df355260c4196383d03fe3656fbfefe4c534ddf478664b1907df192f9e6aa84b74769f5b5ec4fddf89c2a1a7d7039e816045ec',
    'user'
);

INSERT INTO species (species)
VALUES ('Karhu');

INSERT INTO species (species)
VALUES ('Leijona');

INSERT INTO species (species)
VALUES ('Siili');

INSERT INTO origin (origin)
VALUES ('Saksa');

INSERT INTO origin (origin)
VALUES ('Kenia');

INSERT INTO origin (origin)
VALUES ('Japani');

INSERT INTO staff (name, role, hire_date)
VALUES ('Hanna Hoituri', 'Hoitaja', '2020-08-10');

INSERT INTO staff (name, role, hire_date)
VALUES ('Kalle Kalamies', 'Hoitaja', '2015-05-11');

INSERT INTO staff (name, role, hire_date)
VALUES ('Lea Lekuri', 'Lääkäri', '2018-03-07');

INSERT INTO diagnosis (diagnosis)
VALUES ('Diabetes');

INSERT INTO diagnosis (diagnosis)
VALUES ('Munuaisen vajaatoiminta');

INSERT INTO animal (name, species_id, gender, birthday, origin_id, diet, staff_id)
VALUES ('Karhu', 1, 'Naaras', '2017-02-15', 1, 'Liha, kasvis', 1);

INSERT INTO animal (name, species_id, gender, birthday, origin_id, diet, staff_id)
VALUES ('Siili', 3, 'Uros', '2009-12-02', 1, 'Siilinruoka', 2);

INSERT INTO animal_diagnosis (animal_id, diagnosis_id)
VALUES (1, 1);

INSERT INTO animal_diagnosis (animal_id, diagnosis_id)
VALUES (2, 1);

INSERT INTO animal_diagnosis (animal_id, diagnosis_id)
VALUES (2, 2);

INSERT INTO medical_record (record, animal_id, user_id)
VALUES ('Ruoka, lääke annettu.', 1, 2);

INSERT INTO medical_record (record, animal_id, user_id)
VALUES ('Hammastarkistus tehty.', 2, 3);
