from database import Repository
from locator import PlaceExtractor, ScoreCalculator
from tweet import Tweet

class Processor:

    def __init__(self):
        self.communes, self.places = \
            Repository.all_users_with_places()

    def process(self, tweet):
        stored_tweet = Repository.create(tweet)

        if stored_tweet is None:
            return None

        username = tweet.user.username
        sorted_scores = self.get_potential_places(tweet)
        actual_places = self.places[username]
        actual_communes = self.communes[username]

        # Iterate over all the potential places by score to find commune
        for potential_place, score in sorted_scores:
            potential_commune = potential_place

            # If the place is a commune, restrict all places to be inside that commune
            if potential_commune in actual_communes:
                actual_places = actual_communes[potential_place]

                # We found a commune, do not look for any more
                break

        # Iterate over all the potential places by score
        for potential_place, score in sorted_scores:

            # Check if the potential place is in the actual places
            if potential_place in actual_places:
                actual_place = actual_places[potential_place]

                # Create a relation between the tweet and the place
                position = self.link_tweet_to_place(tweet, actual_place)

                # We found a place, so lets move on to the next weet
                break

        return Repository.read(tweet.id)

    def process_many(self, tweets):
        for index, tweet in enumerate(tweets):
            self.process(tweet)

    def link_tweet_to_place(self, tweet, place):
        return Repository.map_place_to_tweet(tweet, place.id)

    def get_potential_places(self, tweet):
        scores = {}
        potential_places = PlaceExtractor(tweet).find_potential_places()

        for potential_place in potential_places:
            score = ScoreCalculator(tweet).for_word(potential_place)
            scores[potential_place] = score

        sorted_scores = sorted(scores.items(), reverse=True, key=lambda score: score[1])
        return sorted_scores
