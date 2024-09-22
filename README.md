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
At the moment you can create a new user from the login page to enable easy testing. Database allows admin users, but for now new users are basic users by default and no admin features have been implemented. If this was a real application only admins could add new users, which would require adding admin manually into the database.

When logged in, there is a dummy-link/page to add a new animal into the zoo, but it doesn't yet add it into the database, even though the tables exist in schema.sql. None of the advanced features (medical records, search etc.) has not yet been implemented.

--

How to use:

Clone this repository into your own computer and locate its root directory. Create .env -file and add following information:

DATABASE_URL=<local-database-location>
SECRET_KEY=<secret-key>

Next, activate the virtual environment and install the dependencies for the application with commands:
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt

Define database scheme with command:
$ psql < schema.sql

Now you can start the application with command:
$ flask run


