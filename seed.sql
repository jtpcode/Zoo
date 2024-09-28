INSERT INTO users (username, password, role)
VALUES (
    'admin',
    'scrypt:32768:8:1$GFUKCZNDlSBdP4en$5c7b143831d859c687cfee818f6eb15bd806b2d1e82aaa76c981fb6a7f763b508a8f019e5a05584274d3f8aa2faa8ef051928d887cc5c94de044094be7e002e9',
    'admin'
);

INSERT INTO species (species)
VALUES ('Karhu');

INSERT INTO species (species)
VALUES ('Leijona');

INSERT INTO origin (origin)
VALUES ('Saksa');

INSERT INTO origin (origin)
VALUES ('Kenia');

INSERT INTO staff (name, role, hire_date)
VALUES ('Hanna Hoituri', 'Hoitaja', '2020-08-10');

INSERT INTO staff (name, role, hire_date)
VALUES ('Lea Lekuri', 'Lääkäri', '2018-03-07');

INSERT INTO diagnosis (name)
VALUES ('Diabetes');

INSERT INTO diagnosis (name)
VALUES ('Munuaisen vajaatoiminta');
