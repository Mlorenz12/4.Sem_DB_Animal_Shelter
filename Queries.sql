/*
For the queries, which are copied from the code I used :something
to show you that this variable is dynamic and filling those dynamic
variables which values is left to the ORM
You will have to replace them with actual strings or ints to use them in a normal SQL-tool
I tried to name them so you know what these variables are about
*/

CREATE TEMP VIEW IF NOT EXISTS Fraud_submission as
SELECT d.first_name, d.last_name, money.amount, s.shelter_name, money.timestamp 
FROM donors as d 
INNER JOIN donations as money
ON d.id = money.donor
INNER JOIN shelters as s
ON s.id = money.shelter
WHERE strftime('%Y %m',money.timestamp) = (
    SELECT strftime('%Y %m','now'));

/*
    This Query creates a temporary view 
    if the View with this name does not already exist
    (it will delete itself after disconnecting from the database)
    This view is a overview over the amount and time a particular person
*/

SELECT animal_food.animal_id, animal_food.food_id, supplier_food.supplier_id, addresses.street, addresses.number, addresses.city
FROM animal_food
JOIN supplier_food
ON animal_food.food_id = supplier_food.food_id
JOIN suppliers
ON supplier_food.supplier_id = suppliers.id
JOIN addresses
ON suppliers.address = addresses.id
WHERE animal_food.animal_id = 2;

/*
This Query ...
*/


--copied from the project--
select shelters.shelter_name, a.city,a.zip_code,a.street,a.number 
from shelters, addresses as a
where a.id == shelters.address

 /*
    The select statement gets all the relevant information from the tabels shelters and addresses
    by querying the needed columens where the ID of addresses is equal
    to the forgein key written in shelters.addresses
 */

--copied from the project--
select v.id, v.firstname,v.lastname, s.shelter_name
from volunteers as v, shelters as s
where v.firstname == :fn \
and v.lastname == :ln \
and v.password == :pd \
and s.id == v.shelter

/*
    This Query is dynamic. :XX are variables, which get filled in
    inside the actual python
    This Query gets a specific person with its name and the shelter
    he/she is working in, if the provided information is correct (password check).
*/

--in the code we used the ORM for this--
DELETE FROM volunteers
WHERE volunteers.id = :current_object_id
/*
    In the code we used the ORM to delete a person from the volunteers list
    by just sending the id of the requesting person through the ORM
    This SQL-statement shows the way this works
*/

--in the code we used the ORM for this--
UPDATE volunteers
SET shelter = (
    SELECT shelters.id
    FROM shelters
    WHERE shelters.shelter_name = :wanted_shelter 
    --e.g. 'Munich' (in the actual code the form already translates the text to a value which matches the shelter_ID)
)
WHERE volunteers.id = :current_volu_id
/*
    In the code we used the ORM to update a shelter from the volunteers list
    by just sending the id of the requesting person and 
    the shelter he/she wants to go to through the ORM and 
    update the foreign key to the new shelter id
    This SQL-statement shows the way this works
*/

--in the code we used the ORM for this--
INSERT INTO volunteers
VALUES (12, "Karl", "Ochse", "m", "1954-12-12 23:45:00", 1, 2);
/*
    This a simple statement to insert a new volunteer
    in the code all this data gets filed by a submission form
    and we get the name, birthday etc. from a POST request
*/