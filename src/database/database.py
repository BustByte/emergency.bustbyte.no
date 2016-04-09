import os
import sqlite3
from config import configuration

def get_connection():
    return sqlite3.connect(
        ':memory:' if os.environ['TEST'] else
        configuration['database']['location'],
        check_same_thread=False,
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
    )

class Database:

    connection = get_connection()

    @classmethod
    def run_schema(cls, schema):
        cur = Database.connection.cursor()
        current_directory = os.path.dirname(os.path.realpath(__file__))
        with open(current_directory + '/schemas/' + schema, 'r') as schema:
            sql = schema.read()
        cur.executescript(sql)
        Database.connection.commit()

    @classmethod
    def setup(cls):
        cls.run_schema('setup.sql')

    @classmethod
    def tear_down(cls):
        Database.connection = get_connection()

    @classmethod
    def table_exists(cls, name):
        cur = Database.connection.cursor()
        cur.execute('''SELECT name FROM sqlite_master;''')
        Database.connection.commit()
        returned = cur.fetchone()
        return returned is not None

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
