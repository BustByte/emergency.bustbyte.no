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
	WHERE content LIKE "%kniv%"
````

### All places within the district of a Twitter user
````sql
SELECT DISTINCT places.id, places.commune_id, places.name, communes.name FROM users
    JOIN districts on users.district = districts.id
    JOIN commune_in_district on districts.id = commune_in_district.district_id
    JOIN communes on commune_in_district.commune_id = communes.id
    JOIN places on communes.id = places.commune_id
    WHERE users.username = 'opsenfollo';
````

### Check location information for a tweet.
````sql
SELECT * from tweets
   JOIN tweet_in_place on tweets.id = tweet_in_place.tweet_id
   JOIN places on tweet_in_place.place_id = places.id
````

### Delete all mappings between tweets and places
````sql
DELETE FROM tweet_in_place
````

### Check if it only exist one place for each tweet
````sql
SELECT COUNT(DISTINCT tweet_id) AS place FROM tweet_in_place;
SELECT COUNT(*) FROM tweet_in_place;
````

### Merge tweets and position into a single table
````sql
INSERT INTO place_tweet (tweet_id, username, content, timestamp, latitude, longitude) 
	SELECT tweets.id, tweets.username, tweets.content, tweets.timestamp, places.latitude, places.longitude FROM tweets 
		JOIN users ON users.username = tweets.username 
		LEFT OUTER JOIN tweet_in_place ON tweets.id = tweet_in_place.tweet_id
		LEFT OUTER JOIN places on tweet_in_place.place_id=places.id
````
