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

    def test_it_can_tear_down_the_schema(self):
        Database.tear_down()
        self.assertEqual(Database.table_exists('users'), False)
        self.assertEqual(Database.table_exists('tweets'), False)
        self.assertEqual(Database.table_exists('communes'), False)
        self.assertEqual(Database.table_exists('districts'), False)
