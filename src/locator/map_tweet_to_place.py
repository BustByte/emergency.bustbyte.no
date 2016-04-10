import operator
from database import Repository
from locator import PlaceExtractor
from locator import ScoreCalculator

tweets = Repository.all()

for tweet in tweets:

    places = PlaceExtractor(tweet).find_potential_places()
    scores = {}

    for place in places:
        score = ScoreCalculator(tweet).for_word(place)
        scores[place] = score

    sorted_scores = sorted(scores.items(), reverse=True, key=lambda score: score[1])

    districts = {}

    for sorted_score in sorted_scores:

        tweet_place = sorted_score[0]
        username = Tweet.user.username
        
        if username in districts:
            places = districts[username]
        else:
            districts[username] = Repository.read_places(username)
            places = districts[username]

        for place in places:
            if place.name == tweet_place:
                Repository.map_place_to_tweet(tweet.id, place.id) 

    print(scores)

    #print(scores)

    print("\n\n")
