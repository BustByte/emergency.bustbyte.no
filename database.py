import sqlite3
from config import configuration

class Database:

    connection = sqlite3.connect(
        configuration['database']['location'],
        check_same_thread=False,
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
    )

    @classmethod
    def setup(cls):
        Database.connection.row_factory = sqlite3.Row
        cur = Database.connection.cursor()
        cur.execute('''create table if not exists tweets(
            id text primary key,
            username text,
            content text,
            timestamp timestamp
        )''')

    @classmethod
    def save(cls, tweet):
        cur = Database.connection.cursor()
        try:
            cur.execute('''
                insert into tweets values (
                    :id,
                    :content,
                    :username,
                    :timestamp
                )''', cls.to_row(tweet))
        except sqlite3.IntegrityError:
            return None
        Database.connection.commit()
        return cur.lastrowid

    @classmethod
    def to_row(cls, tweet):
        row = {}
        row['id'] = tweet.id
        row['username'] = tweet.username
        row['content'] = tweet.content
        row['timestamp'] = tweet.timestamp
        return row 
