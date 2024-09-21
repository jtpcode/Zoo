# Zoo
The idea of this application is to serve the staff of an imaginary Zoo. Once logged in a member of the staff can manipulate the database 
to for example:
- add new animals (species, origin, name, birthday, special diet, health status...)
- search information about animals based on name, species, origin..
- add a message (with timestamp and who wrote the message) concerning animal care, for example "Ben the bear was fed and given antibiotics"
- see the messages concerning a specific animal
- browse messages with certain keywords or dates
- add new staff members as users to the application
- ...

The app could include also for example food/supply stock etc.

How to use:

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla:
$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla:
$ flask run


At the moment you can create a new user from the homepage to enable easy testing. Database allows admin users, but for now new users are basic users by default and no admin features have been implemented. If this was a real application only admins could add new users, which would require adding admin user manually into the database.
