CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
login text NOT NULL,
password text NOT NULL
);

CREATE TABLE IF NOT EXISTS tracks (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
autor text NOT NULL,
image text
);

CREATE TABLE IF NOT EXISTS playlists (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
image text,
tracks text
);

CREATE TABLE IF NOT EXISTS comments (
id integer PRIMARY KEY AUTOINCREMENT,
userid integer,
trackid integer,
content text NOT NULL
);