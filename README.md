# Zoo
The idea of this application is to serve the staff of an imaginary Zoo. Once logged in a member of the staff can manipulate the database 
to for example:
- add new staff members as application users
- add new animals (unique "ssn", species, origin, name, birthday, special diet, health status...)
- list all animals
- search information about animals based on "ssn", name, species, origin..
- add a medical record (with timestamp and who wrote the message) concerning animal care, for example "Ben the bear was fed and given antibiotics"
- see the medical records concerning a specific animal
- search medical records with certain keywords or dates
- ...

NOTE:
You can use the provided seed.sql to create initial admin user (username, password = admin) and some data into needed tables. Only admin can add new staff members. New application users are regular users by default, not yet possible to change into admin status.

Medical records, search etc. have not yet been implemented.

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

