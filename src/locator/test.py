from database import Repository
from locator import PlaceExtractor
from locator import ScoreCalculator

tweets = Repository.all()

for tweet in tweets:
    print(tweet.content)
    places = PlaceExtractor(tweet).find_potential_places()
    for place in places:
        score = ScoreCalculator(tweet).for_word(place)
        print(place, score, "\n\n")
