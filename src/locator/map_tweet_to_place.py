import operator
from database import Repository
from locator import PlaceExtractor, ScoreCalculator
from tweet import Tweet

tweets = Repository.all()
places = Repository.all_users_with_places()

def get_potential_places(tweet)
    scores = {}
    potential_places = PlaceExtractor(tweet).find_potential_places()

    for potential_place in potential_places:
        score = ScoreCalculator(tweet).for_word(potential_place)
        scores[potential_place] = score
    sorted_scores = sorted(scores.items(), reverse=True, key=lambda score: score[1])

    return sorted_scores

for tweet in tweets:

    username = tweet.user.username
    sorted_scores = get_potential_places(tweet)

    for potential_place, score in sorted_scores:

        if potential_place in places[username]:
            place = places[username][potential_place]
            Repository.map_place_to_tweet(tweet.id, place.id) 

            break # Move on to next tweet

    print(scores)
    print("\n\n")
