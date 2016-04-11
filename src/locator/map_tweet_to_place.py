import operator
from database import Repository
from locator import PlaceExtractor, ScoreCalculator
from tweet import Tweet

tweets = Repository.all()
communes, places = Repository.all_users_with_places()

def get_potential_places(tweet):
    scores = {}
    potential_places = PlaceExtractor(tweet).find_potential_places()

    for potential_place in potential_places:
        score = ScoreCalculator(tweet).for_word(potential_place)
        scores[potential_place] = score
    sorted_scores = sorted(scores.items(), reverse=True, key=lambda score: score[1])

    return sorted_scores

for index, tweet in enumerate(tweets):

    username = tweet.user.username
    sorted_scores = get_potential_places(tweet)
    actual_places = places[username]
    actual_communes = communes[username]
    actual_place = None

    # Iterate over all the potential places by score to find commune
    for potential_place, score in sorted_scores:
        potential_commune = potential_place
        if potential_commune in actual_communes:
            print("Avgrenser til kommune:", potential_commune)
            actual_places = actual_communes[potential_place]

            # We found a commune, do not look for any more
            break

    # Iterate over all the potential places by score
    for potential_place, score in sorted_scores:

        # Check if the potential place is in the actual places
        if potential_place in actual_places:
            actual_place = actual_places[potential_place]
            Repository.map_place_to_tweet(tweet.id, actual_place.id) 

            # We found a place, so lets move on to the next weet
            break

    #print("TWEET NUMBER:", index)
    #print(sorted_scores)
    #print("\n\n")
