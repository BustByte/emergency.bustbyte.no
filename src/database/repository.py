from database import Mapper
from database import Database
from position import Place
import sqlite3
from collections import defaultdict

class Repository:

    @classmethod
    def create(cls, tweet):
        cur = Database.connection.cursor()
        tweet_row = Mapper.to_row(tweet)
        try:
            row = defaultdict(lambda: None, tweet_row)
            cur.execute('''
                INSERT INTO tweets
                (id, username, name, content, timestamp) values
                (:id, :username, :name, :content, :timestamp)''',
                row 
            )
        except sqlite3.IntegrityError:
            return None
        Database.connection.commit()
        return cur.lastrowid

    @classmethod
    def read(cls, tweet_id):
        cur = Database.connection.cursor()
        cur.execute('SELECT * FROM place_tweet WHERE id = :id',
            {'id': str(tweet_id)})
        Database.connection.commit()
        row = cur.fetchone()
        if (row == None):
            tweet = Repository.read_orignal_tweet(tweet_id)
        else:
            tweet = Mapper.to_tweet(row)
        return tweet

    @classmethod
    def read_orignal_tweet(cls, tweet_id):
        cur = Database.connection.cursor()
        cur.execute('SELECT * FROM tweets WHERE id = :id',
            {'id': str(tweet_id)})
        Database.connection.commit()
        row = cur.fetchone()
        tweet = Mapper.to_tweet(row)
        return tweet

    @classmethod
    def read_multiple(cls, tweets, query_object):
        tweets = tweets[:900]
        cur = Database.connection.cursor()
        query = '''SELECT * FROM place_tweet WHERE timestamp < :end AND timestamp > :start
            AND latitude NOT NULL and longitude NOT NULL AND
        ('''
        for tweet_id in tweets:
            query += "id = '" + tweet_id + "' OR "
        query += '1 = 0)'
        cur.execute(query, {
            'end': query_object.end_date,
            'start': query_object.start_date
        })
        Database.connection.commit()
        rows = cur.fetchall()
        tweets = [Mapper.to_tweet(row) for row in rows]
        return tweets

    @classmethod
    def get_position(cls, place_id):
        cur = Database.connection.cursor()
        cur.execute("SELECT * FROM places WHERE id = :place", {
            'place': place_id
        })
        Database.connection.commit()
        row = cur.fetchone()
        position = Mapper.to_position(row)
        return position

    @classmethod
    def map_place_to_tweet(cls, tweet, place_id):
        cur = Database.connection.cursor()
        position = Repository.get_position(place_id)
        row = {'tweet_id': str(tweet.id), 'place_id': place_id}

        try:

            cur.execute('''
                INSERT INTO place_tweet (id, username, content, timestamp, latitude, longitude, place_id)
                VALUES  (:tweet_id, :username, :content, :timestamp, :latitude, :longitude, :place_id)
                ''',
                {
                    'tweet_id': tweet.id,
                    'username': tweet.user.username,
                    'content': tweet.content,
                    'timestamp': tweet.timestamp,
                    'latitude': position.latitude,
                    'longitude': position.longitude,
                    'place_id': place_id
                }
            )

        except sqlite3.IntegrityError:
            return None
        Database.connection.commit()
        return cur.lastrowid

    @classmethod
    def search(cls, query_object):
        cur = Database.connection.cursor()
        query = query_object.get('query')
        cur.execute('''SELECT * FROM place_tweet
            WHERE content LIKE :query AND timestamp < :end AND timestamp > :start
            AND latitude NOT NULL AND longitude NOT NULL
            LIMIT 1000''',
            {
                #'query': '*[ ,./:;#@(][{0}{1}]{2}[ ,.\!?:;/\')]*'.format(query[0].lower(), query[0].upper(), query[1:]),
                'query': '%{0}%'.format(query),
                'end'  : query_object.get('endDate'),
                'start': query_object.get('startDate')
            }
        )
        Database.connection.commit()
        rows = cur.fetchall()
        tweets = [Mapper.to_tweet(row) for row in rows]
        return tweets

    @classmethod
    def all(cls):
        cur = Database.connection.cursor()
        cur.execute('''SELECT * FROM place_tweet''')
        Database.connection.commit()
        rows = cur.fetchall()
        tweets = [Mapper.to_tweet(row) for row in rows]
        return tweets

    @classmethod
    def all_between_dates(cls, query_object):
        cur = Database.connection.cursor()
        query = '''SELECT * FROM place_tweet WHERE timestamp < :end AND timestamp > :start AND latitude NOT NULL AND longitude NOT NULL'''
        cur.execute(query, {
            'end': query_object.end_date,
            'start': query_object.start_date
        })
        Database.connection.commit()
        rows = cur.fetchall()
        tweets = [Mapper.to_tweet(row) for row in rows]
        return tweets

    @classmethod
    def all_users_with_places(cls):
        commune_cache, place_cache = ({}, {})
        cur = Database.connection.cursor()
        cur.execute('''SELECT username, communes.name as commune_name, places.id AS id, places.name AS place_name FROM users
            JOIN districts on users.district = districts.id
            JOIN commune_in_district on districts.id = commune_in_district.district_id
            JOIN communes on commune_in_district.commune_id = communes.id
            JOIN places on communes.id = places.commune_id'''
        )
        Database.connection.commit()
        rows = cur.fetchall()

        for row in rows:
            place = Mapper.to_place(row)

            if row['username'] not in place_cache:
                place_cache[row['username']] = {}

            if row['username'] not in commune_cache:
                commune_cache[row['username']] = {}

            if row['commune_name'] not in commune_cache[row['username']]:
                commune_cache[row['username']][row['commune_name']] = {}

            place_cache[row['username']][place.name] = place
            commune_cache[row['username']][place.commune_name][place.name] = place

        return (commune_cache, place_cache)
