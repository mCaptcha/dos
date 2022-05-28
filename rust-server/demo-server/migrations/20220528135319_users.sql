-- Add migration script here
CREATE TABLE IF NOT EXISTS users (
	name VARCHAR(100) NOT NULL,
	password TEXT NOT NULL,
	ID SERIAL PRIMARY KEY NOT NULL
);
