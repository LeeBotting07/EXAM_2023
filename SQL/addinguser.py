import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Accept user data from the registration form
username = input("Enter username: ")
email = input("Enter email: ")
password = input("Enter password: ")
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
firstName = input("Enter first name: ")
lastName = input("Enter last name: ")
phoneNumber = input("Enter phone number: ")
address = input("Enter address: ")

with sqlite3.connect("weather.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO users (username, firstName, lastName, phoneNumber, address, email, password, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (username, firstName, lastName, phoneNumber, address, email, hashed_password, 'user'))  # Role set to 'user'
    con.commit()
