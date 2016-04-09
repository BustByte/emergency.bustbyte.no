import os
import sqlite3
from config import configuration

class Database:

    connection = sqlite3.connect(
            ':memory:' if os.environ['TEST'] else
            configuration['database']['location'],
        check_same_thread=False,
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
    )

    @classmethod
    def create(cls, tweet):
        cur = Database.connection.cursor()
        try:
            cur.execute('''insert into tweets
                (id, username, name, content, timestamp) values
                (:id, :username, :name, :content, :timestamp)''',
                cls.to_row(tweet)
            )
        except sqlite3.IntegrityError:
            return None
        Database.connection.commit()
        return cur.lastrowid
