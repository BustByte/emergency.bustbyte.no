### All tweets within a district
````sql
SELECT * FROM tweets
	JOIN users on tweets.username=users.username
	WHERE users.district = :district_id:
````

### All places within a district
````sql
SELECT districts.name, communes.name, places.name FROM places 
	JOIN commune_in_district on places.commune_id=commune_in_district.commune_id 
	JOIN communes on places.commune_id=communes.id
	JOIN districts on commune_in_district.district_id=districts.id
````

### All tweets containing "kniv"
````sql
SELECT content FROM tweets
	WHERE content LIKE "%kniv%
````