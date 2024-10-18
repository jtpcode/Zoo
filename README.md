# Zoo
The idea of this application is to serve the staff of an Imaginary Zoo. Once logged in a member of the staff can:
- Admin:
    - add new staff members
    - add new app users (new application users are basic users by default)
    - add new animals (unique name, species, origin, birthday, special diet, health status...)
- Basic user:
    - search information about animals based on the unique name
    - add a medical record (with timestamp and who wrote the message) concerning animal care
    - see the medical records concerning a specific animal

There are few origin countries, species and diagnoses in the seed.sql, but in real life all possible countries/species/diagnoses
would be included in the database.

You can use the provided seed.sql to create:
- initial admin user with username, password = admin, admin
- two basic users with username, password = "Hanna Hoituri", hannahoituri and "Kalle Kalamies", kallekalamies
- some data into needed tables.

Medical records (eläintietokanta):
- the names of the animals are unique, so you search using names (at the moment you must know them)

Future development ideas:
- 

--

How to use:

Clone this repository into your own computer and locate its root directory. Create .env -file and add following information:

- DATABASE_URL=<local-database-location>
- SECRET_KEY=<secret-key>

Next, activate the virtual environment and install the dependencies for the application with commands:
- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install -r ./requirements.txt

Define database scheme with command:
- $ psql < schema.sql

Input data into tables with command:
- $ psql < seed.sql

Now you can start the application with command:
- $ flask run

