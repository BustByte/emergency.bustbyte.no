CREATE TABLE tweets(
            id text primary key,
            username text,
            name text,
            content text,
            timestamp text
        );
CREATE TABLE `communes` (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`polygon`	TEXT,
	PRIMARY KEY(id)
);
CREATE TABLE `districts` (
	`id`	INTEGER,
	`name`	TEXT NOT NULL
);
CREATE TABLE "places" (
	"id"	INTEGER,
	"commune_id"	INTEGER,
	"name"	TEXT,
	"latitude"	TEXT,
	"longitude"	TEXT,
	FOREIGN KEY(commune_id) REFERENCES communes (id) );
CREATE TABLE `users` (
	`username`	TEXT NOT NULL,
	`district`	INTEGER NOT NULL,
	FOREIGN KEY(username) REFERENCES tweets(username),
	FOREIGN KEY(district) REFERENCES districts(id)
);
CREATE TABLE `commune_in_district` (
	`commune_id`	INTEGER NOT NULL,
	`district_id`	INTEGER NOT NULL,
	FOREIGN KEY(`commune_id`) REFERENCES `communes`(`id`),
	FOREIGN KEY(`district_id`) REFERENCES `districts`(`id`)
);

CREATE TABLE `tweet_in_place` (
    `tweet_id`  INTEGER NOT NULL,
    `place_id`  INTEGER NOT NULL,
    FOREIGN KEY(tweet_id) REFERENCES tweets(id),
    FOREIGN KEY(place_id) REFERENCES places(id)
);

-- Only run if under test
INSERT INTO users (username, district) VALUES ('opsenoslo', 1);
INSERT INTO districts (id, name) VALUES (1, 'Øst');
INSERT INTO communes (id, name) VALUES (1, 'Oslo');
INSERT INTO commune_in_district (commune_id, district_id) VALUES (1, 1);
INSERT INTO places (id, commune_id, name, latitude, longitude) VALUES (1, 1, "Vestby", "59.3434", "18.3434");


