from unittest import TestCase
from unittest.mock import MagicMock
from database import Database

class TestDatabase(TestCase):

    def test_it_can_setup_the_schema(self):
        Database.setup()
        self.assertEqual(Database.table_exists('users'), True)
        self.assertEqual(Database.table_exists('tweets'), True)
        self.assertEqual(Database.table_exists('communes'), True)
        self.assertEqual(Database.table_exists('districts'), True)
        Database.tear_down()
