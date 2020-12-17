"""Prediction of users based on tweet embeddings"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet
from .models import User

# Creating a function to precict which user said a hypothetical tweet 
def predict_user(user0_name, user1_name, hypo_tweet_text):
    user0 = User.query.filter(User.name == user0_name).one() # this will give us user zero and user one from our database
    user1 = User.query.filter(User.name == user1_name).one()

    user0_vects = np.array([tweet.vect for tweet in user0.tweets]) # these are the vectors for user 0 and one tweets
    user1_vects = np.array([tweet.vect for tweet in user1.tweets]) 
    
    # Vertically stacking (combining the vectors) (gives us our x - training material)
    vects = np.vstack([user0_vects, user1_vects])

    # Generate labesl (either 0 or 1) for the vects array (gives us our y - target vector)
    labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # Train the model and instantiate
    log_reg = LogisticRegression().fit(vects, labels)

    # vectorize the hypothetical tweet
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1) # need to change it from rows to columns so this is done by respaping

    # Returns zero or one depending on the prediction made from the LR model
    return log_reg.predict(hypo_tweet_vect)