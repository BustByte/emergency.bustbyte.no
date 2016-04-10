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
