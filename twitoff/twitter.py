"""Retrieve Tweets, embeddings, and push to our database"""
from os import getenv
# print(getenv("TWITTER_API_KEY"))
import tweepy  # to interact with the twitter API
import spacy  # will use later
from .models import DB, Tweet, User

# print(getenv("TWITTER_API_KEY"))
TWITTER_AUTH = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"), 
    getenv("TWITTER_SECRET"))
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load("my_model")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        """Adds user with username 'username' to our database"""
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # TODO - fix assumption on continuously new tweets
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode="extended")

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text,
                             vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        DB.session.commit()











# """Retrieve tweets, embedding, and push to database"""
# from os import getenv
# import tweepy #Used to intercact with twitter api
# import spacy
# from .models import DB, Tweet, User


# # Authenticating our API key    Something is wrong here below
# TWITTER_AUTH = tweepy.OAuthHandler(
#     getenv("TWITTER_API_KEY"), getenv("TWITTER_API_KEY_SECRET"))
# TWITTER = tweepy.API(TWITTER_AUTH)

# nlp = spacy.load("my_model")

# # This will return a 96 numberical value
# def vectorize_tweet(tweet_text):
#     return nlp(tweet_text).vector

# def add_or_update_user(username):
#     try:
#         """adds user with username 'username' to our database"""
#         twitter_user = TWITTER.get_user(username)
#         # We want to add the twitter user to our model but we want to make 
#         # sure they dont already exist in our database
#         db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
#         # Now we need to actually add the user to our database
#         DB.session.add(db_user)

#         # Grabbing the users tweets
#         tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='Extended') 

#         if tweets:
#             db_user.newest_tweet_id = tweets[0].id

#         # Add the tweets and iterate through them and assign them to our user through the database
#         for tweet in tweets:
#             vectorized_tweet = vectorize_tweet(tweet.text)
#             db_tweet = Tweet(id=tweet.id, text=tweet.text, vect=vectorized_tweet)
#             db_user.tweets.append(db_tweet) # Connect the tweet to the user 
#             DB.session.add(db_tweet) # Add the tweet to our database

#         # We need to commit our changes
#         DB.session.commit()
#     except Exception as e:
#         print("Error processing {}: {}".format(username, e))
#         raise e
#     else: 
#         DB.session.commit()
