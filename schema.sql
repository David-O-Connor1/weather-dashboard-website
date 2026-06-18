DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- DROP TABLE IF EXISTS expenses;

-- CREATE TABLE expenses
-- (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     amount TEXT NOT NULL,
--     description TEXT NOT NULL,
--     category INTEGER NOT NULL,
--     date TEXT NOT NULL,
--     user_id INTEGER NOT NULL,
--     FOREIGN KEY(user_id) REFERENCES users(id)
-- );