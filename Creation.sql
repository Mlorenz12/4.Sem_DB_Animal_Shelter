/*
This is a complete code to replicate the database-schema used in the application
The execution of the code will create a empty database
Please use the provided .db file
*/

CREATE TABLE "addresses" (
	"id"	INTEGER NOT NULL,
	"country_code"	VARCHAR(2) NOT NULL,
	"zip_code"	VARCHAR(10) NOT NULL,
	"city"	VARCHAR(20) NOT NULL,
	"street"	VARCHAR(20) NOT NULL,
	"number"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "animal_food" (
	"animal_id"	INTEGER,
	"food_id"	INTEGER,
	FOREIGN KEY("animal_id") REFERENCES "animals"("id"),
	FOREIGN KEY("food_id") REFERENCES "food"("id")
);

CREATE TABLE "animals" (
	"id"	INTEGER NOT NULL,
	"animal_name"	VARCHAR(20) NOT NULL,
	"gender"	VARCHAR(1) NOT NULL,
	"brought_in"	DATETIME,
	"taken_at"	DATETIME,
	"shelter"	INTEGER NOT NULL,
	"species_id"	INTEGER NOT NULL,
	"taken_by"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("shelter") REFERENCES "shelters"("id"),
	FOREIGN KEY("species_id") REFERENCES "species"("id"),
	FOREIGN KEY("taken_by") REFERENCES "takers"("id")
);

CREATE TABLE "donations" (
	"amount"	INTEGER NOT NULL,
	"shelter"	INTEGER NOT NULL,
	"donor"	INTEGER NOT NULL,
	"timestamp"	DATETIME NOT NULL,
	PRIMARY KEY("shelter","donor","timestamp")
);

CREATE TABLE "donors" (
	"id"	INTEGER NOT NULL,
	"iban"	VARCHAR(40) NOT NULL,
	"first_name"	VARCHAR(20) NOT NULL,
	"last_name"	VARCHAR(20) NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "food" (
	"id"	INTEGER NOT NULL,
	"description"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "managers" (
	"id"	INTEGER NOT NULL,
	"first_name"	VARCHAR(20) NOT NULL,
	"last_name"	VARCHAR(20) NOT NULL,
	"gender"	VARCHAR(1) NOT NULL,
	"birthday"	DATETIME,
	"shelter"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("shelter") REFERENCES "shelters"("id")
);

CREATE TABLE "shelters" (
	"id"	INTEGER NOT NULL,
	"shelter_name"	VARCHAR(20) NOT NULL,
	"founded_at"	DATETIME,
	"vet"	INTEGER,
	"address"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("vet") REFERENCES "vets"("id"),
	FOREIGN KEY("address") REFERENCES "addresses"("id")
);

CREATE TABLE "species" (
	"id"	INTEGER NOT NULL,
	"species_name"	VARCHAR(20) NOT NULL,
	"sup_species"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("sup_species") REFERENCES "species"("id")
);

CREATE TABLE "supplier_food" (
	"supplier_id"	INTEGER,
	"food_id"	INTEGER,
	FOREIGN KEY("supplier_id") REFERENCES "suppliers"("id"),
	FOREIGN KEY("food_id") REFERENCES "food"("id")
);

CREATE TABLE "supplier_shelter" (
	"supplier_id"	INTEGER,
	"shelter_id"	INTEGER,
	FOREIGN KEY("supplier_id") REFERENCES "suppliers"("id"),
	FOREIGN KEY("shelter_id") REFERENCES "shelters"("id")
);

CREATE TABLE "suppliers" (
	"id"	INTEGER NOT NULL,
	"iban"	VARCHAR(40) NOT NULL,
	"address"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("address") REFERENCES "addresses"("id")
);

CREATE TABLE "takers" (
	"id"	INTEGER NOT NULL,
	"first_name"	VARCHAR(20) NOT NULL,
	"last_name"	VARCHAR(20) NOT NULL,
	"address"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("address") REFERENCES "addresses"("id")
);

CREATE TABLE "vets" (
	"id"	INTEGER NOT NULL,
	"first_name"	VARCHAR(20) NOT NULL,
	"last_name"	VARCHAR(20) NOT NULL,
	"gender"	VARCHAR(1) NOT NULL,
	"birthday"	DATETIME,
	"address"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("address") REFERENCES "addresses"("id")
);

CREATE TABLE "volunteers" (
	"id"	INTEGER NOT NULL,
	"firstname"	VARCHAR(20) NOT NULL,
	"lastname"	VARCHAR(20) NOT NULL,
	"gender"	VARCHAR(1) NOT NULL,
	"birthday"	DATETIME NOT NULL,
	"password"	VARCHAR(20) NOT NULL,
	"shelter"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("shelter") REFERENCES "shelters"("id")
);

CREATE UNIQUE INDEX "iban_idx" ON "donors" (
	"iban" ASC
);

CREATE INDEX "species_idx" ON "animals" (
	"species_id"
);

CREATE VIEW IF NOT EXISTS Fraud_submission as
SELECT d.first_name, d.last_name, money.amount, s.shelter_name, money.timestamp 
FROM donors as d 
INNER JOIN donations as money
ON d.id = money.donor
INNER JOIN shelters as s
ON s.id = money.shelter
WHERE strftime('%Y %m',money.timestamp) = (
    SELECT strftime('%Y %m','now'));