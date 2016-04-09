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
            name text,
            content text,
            timestamp text
        )''')

    @classmethod
    def save_all(cls, tweets):
        for tweet in tweets:
            cls.save(tweet)

    @classmethod
    def save(cls, tweet):
        cur = Database.connection.cursor()
        try:
            cur.execute('''
                insert into tweets values (
                    :id,
                    :username,
                    :name,
                    :content,
                    :timestamp
                )''', cls.to_row(tweet))
        except sqlite3.IntegrityError:
            #print('Already stored %s. Skipping.' % tweet.id)
            return None
        Database.connection.commit()
        return cur.lastrowid

    @classmethod
    def to_row(cls, tweet):
        row = {}
        row['id'] = tweet.id
        row['content'] = tweet.content
        row['timestamp'] = tweet.timestamp
        row['username'] = tweet.user.username
        row['name'] = tweet.user.name
        return row 
