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
        cur.execute('''SELECT * FROM tweets 
            JOIN users ON users.username = tweets.username 
            WHERE id = :id AND users.username not NULL
        ''', {'id': tweet_id})
        Database.connection.commit()
        row = cur.fetchone()
        tweet = Mapper.to_tweet(row)
        return tweet

    @classmethod
    def search(cls, query_object):
        cur = Database.connection.cursor()
        cur.execute('''SELECT * FROM tweets
            JOIN tweet_in_place ON tweet_in_place.tweet_id = tweets.id
            JOIN places ON tweet_in_place.place_id = places.id
            WHERE content LIKE :query AND timestamp < :end AND timestamp > :start LIMIT 500''',
            {
                'query': '% {0} %'.format(query_object.get('query')),
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
        cur.execute('''SELECT * FROM tweets LIMIT 200''')
        Database.connection.commit()
        rows = cur.fetchall()
        tweets = [Mapper.to_tweet(row) for row in rows]
        return tweets

    @classmethod
    def read_places(cls, username):
        cur = Database.connection.cursor()
        cur.execute('''SELECT places.id AS id, places.name AS place_name, communes.name AS commune_name FROM users
            JOIN districts on users.district = districts.id
            JOIN commune_in_district on districts.id = commune_in_district.district_id
            JOIN communes on commune_in_district.commune_id = communes.id
            JOIN places on communes.id = places.commune_id
            WHERE users.username = ':username';''', {
                'username': username
            }
        )
        Database.connection.commit()
        rows = cur.fetchall()
        places = [Mapper.to_place(row) for row in rows]
        return places
