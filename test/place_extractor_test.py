from unittest import TestCase
from unittest.mock import MagicMock
from locator import PlaceExtractor

class TestPlaceExtractor(TestCase):

    def setUp(self):
        self.tweet = MagicMock(content=None)

    def test_it_extracts_no_places_if_empty_string_is_given(self):
        self.tweet.content = ''
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, [])

    def test_it_handles_words_with_multiple_whitespace_characters_in_front_of_it(self):
        self.tweet.content = 'Nødetatene på stedet.  Det er trolig snakk om røyknedslag fra pipe etter fyring i peisen.'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Det', 'Nødetatene'])

    def test_it_extracts_words_with_capital_letter(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front', 'Trondheim'])

    def test_it_does_not_extract_words_with_one_letter(self):
        self.tweet.content = 'Front mot front kollisjon i A'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front'])

    def test_it_does_not_extract_words_with_only_capital_letters(self):
        self.tweet.content = 'UP har hatt kontroll i Trondheim'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Trondheim'])

    def test_it_does_not_extract_words_with_numbers(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim1'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front'])

    def test_it_removes_trailing_exclamation_point(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim!'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front', 'Trondheim'])

    def test_it_removes_any_trailing_full_stop(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim.'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front', 'Trondheim'])

    def test_it_removes_any_trailing_comma(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim,'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front', 'Trondheim'])

    def test_it_removes_any_trailing_question_mark(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim?'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front', 'Trondheim'])

    def test_it_removes_multiple_trailing_symbols(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim??'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front', 'Trondheim'])

    def test_it_does_not_remove_dash_in_middle_of_word(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim-Tiller!'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places, ['Front', 'Trondheim-Tiller'])

    def test_it_does_not_include_duplicate_words(self):
        self.tweet.content = 'Front mot front kollisjon i Trondheim Trondheim'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places,  ['Front', 'Trondheim'])

    def test_it_sorts_places_alphabetically(self):
        self.tweet.content = 'Baker i Akerselva i Oslo'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places,  ['Akerselva', 'Baker', 'Oslo'])

    def test_it_finds_words_with_colon(self):
        self.tweet.content = '23:14: Oslo, Bjørvika: Hei Akerselva: i: Oslo'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places,  ['Akerselva', 'Bjørvika', 'Hei', 'Oslo'])

    def test_it_finds_first_word_with_colon(self):
        self.tweet.content = 'Bjørvika: Angrep mann i 20-årene. Oslo: hei.'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places,  ['Angrep', 'Bjørvika', 'Oslo'])

    def test_it_finds_words_with_slash(self):
        self.tweet.content = 'Brann i bil på Jessheim/Gardermoen.'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places,  ['Brann', 'Gardermoen', 'Jessheim'])

    def test_it_finds_word_with_slash_where_first_word_is_lowercase(self):
        self.tweet.content = 'Brann i bil v/Gardermoen.'
        places = PlaceExtractor(self.tweet).find_potential_places()
        self.assertEqual(places,  ['Brann', 'Gardermoen'])
