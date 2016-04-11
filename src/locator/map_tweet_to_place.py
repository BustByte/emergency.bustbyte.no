import operator
from database import Repository
from tweet import Tweet
from locator import PlaceExtractor, ScoreCalculator

tweets = Repository.all()
districts = {}

for tweet in tweets:

    places = PlaceExtractor(tweet).find_potential_places()
    scores = {}

    for place in places:
        score = ScoreCalculator(tweet).for_word(place)
        scores[place] = score

    sorted_scores = sorted(scores.items(), reverse=True, key=lambda score: score[1])

    for sorted_score in sorted_scores:

        tweet_place = sorted_score[0]
        username = tweet.user.username
        
        if username in districts:
            print("hit the cache", username)
            places = districts[username]
        else:
            print("missed the cache", username)
            eirik_places = Repository.read_places(username)
            quick_places = {}

            for eirik_place in eirik_places:
                quick_places[eirik_place.name] = eirik_place
            
            districts[username] = quick_places

            places = districts[username]

        if place in places:
            place = places[place]
            if place.name == tweet_place:
                Repository.map_place_to_tweet(tweet.id, place.id) 

                # Move on to next tweet
                break

    print(scores)

    print("\n\n")
