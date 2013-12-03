CREATE TABLE movie (
	id INTEGER PRIMARY KEY,
	title TEXT,
	year INTEGER,
);

CREATE TABLE director (
	id INTEGER PRIMARY KEY,
	first_name TEXT,
	last_name TEXT,
	fullname TEXT
);

CREATE TABLE actor (
	id INTEGER PRIMARY KEY,
	first_name TEXT,
	last_name TEXT,
	fullname TEXT
);

CREATE TABLE genre (
	id INTEGER PRIMARY KEY,
	genre_name TEXT
);

CREATE TABLE format (
	id INTEGER PRIMARY KEY,
	format_type TEXT
);

CREATE TABLE movie_director (
	movie_id INTEGER,
	director_id INTEGER
);

CREATE TABLE movie_actor (
	movie_id INTEGER,
	actors_id INTEGER
);

CREATE TABLE movie_genre (
	movie_id INTEGER,
	genre_id INTEGER
);

CREATE TABLE movie_format (
	movie_id INTEGER,
	format_id INTEGER
);

.schema