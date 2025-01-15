-- Users Table

DROP TABLE IF EXISTS users;

ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user';


CREATE TABLE users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    phoneNumber TEXT,
    address TEXT
);