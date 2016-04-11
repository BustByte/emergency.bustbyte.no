from unittest import TestCase
from unittest.mock import MagicMock
from listeners import EpochConverter

class TestEpochConverter(TestCase):

    def setUp(self):
        pass

    def test_it_can_convert_a_valid_epoch_to_a_date_string(self):
        epoch = 1460390582938
        date = EpochConverter.to_date_string(epoch)
        self.assertEqual(date, '2016-04-11 18:03:02')

    def test_it_can_convert_an_old_yet_valid_epoch_to_a_datetime(self):
        epoch = 1060390582938
        date = EpochConverter.to_date_string(epoch)
        self.assertEqual(date, '2003-08-09 02:56:22')

    def test_it_raises_exception_if_epoch_is_invalid(self):
        epoch = 'invalid epoch'
        with self.assertRaises(ValueError):
            date = EpochConverter.to_date_string(epoch)

    def test_it_handles_strings_as_input(self): 
        epoch = '1460390582938'
        date = EpochConverter.to_date_string(epoch)
        self.assertEqual(date, '2016-04-11 18:03:02')
