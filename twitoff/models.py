"""SQLAlchemy models and utility functions for Twitoff"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB = SQLAlchemy()
MIGRATE = Migrate()


# User Table (in relational database the table is "user")
class User(DB.Model):
    """Twitter users corresponding to Tweets"""
    # primary id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    
    # name column
    name = DB.Column(DB.String, nullable=False)
    
    # keeps track of users most recent tweet
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)


# Tweet Table (in relational database the table is "tweet")
class Tweet(DB.Model):
    """Tweet Text and Data"""
    # primary id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    
    # text column of character length 300 (unicode)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    
    # foreign key - user.id
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)





# """SQLAlchemy models and utility functions for Twitoff"""

# from flash_sqlalchemy import SQLAlchemy

# BD = SQLAlchemy() #This DB object defines our database and allows us to instantiate a database

# # Creating a table inheriting from BD.model
# class User(DB.model):
#     """Twitter users corresponding to tweets"""
#     # Primary ID column
#     id = DB.Column(BD.BigInteger, primart_key=True) # Relational data base so there are keys
#     # Name column
#     name = DB.Column(DB.String, nullable=False)

#     def __repr__(self):
#         return "<User: {}>".format(self.name)





# Creating another table, tweet table

# """SQLAlchemy models and utility functions for Twitoff"""
# from flask_sqlalchemy import SQLAlchemy
# DB = SQLAlchemy()
# # User Table
# class User(DB.Model):
#     """Twitter users corresponding to Tweets"""
#     # primary id column
#     id = DB.Column(DB.BigInteger, primary_key=True)
#     # name column
#     name = DB.Column(DB.String, nullable=False)
#     def __repr__(self):
#         return "<User: {}>".format(self.name)

# # Tweet Table
# class Tweet(DB.Model):
#     """Tweet text and data"""
#     # primary Id column
#     id = DB.Column(DB.BigInteger, primary_keys=True)
#     # Text column of character length 300
#     text = DB.Column(DB.Unicode(300))
#     # Use a foreign key to connect userrs and tweets
#     user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
#     user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))


# """SQLAlchemy models and utility functions for Twitoff"""
# from flask_sqlalchemy import SQLAlchemy
# DB = SQLAlchemy()
# # User Table (in relational database the table is "user")
# class User(DB.Model):
#     """Twitter users corresponding to Tweets"""
#     # primary id column
#     id = DB.Column(DB.BigInteger, primary_key=True)
#     # name column
#     name = DB.Column(DB.String, nullable=False)
#     # Newest tweet id will prevent repeted tweets, this will keep track of the users newest tweet
#     newest_tweet_id = DB.Column(DB.BigInteger)
#     def __repr__(self):
#         return "<User: {}>".format(self.name)
# # Tweet Table (in relational database the table is "tweet")
# class Tweet(DB.Model):
#     """Tweet Text and Data"""
#     # primary id column
#     id = DB.Column(DB.BigInteger, primary_key=True)
#     # text column of character length 300 (unicode)
#     text = DB.Column(DB.Unicode(300))
#     vect = DB.Column(DB.PickleType, nullable=False)
#     # foreign key - user.id
#     user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
#         'user.id'), nullable=False)
#     user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
#     def __repr__(self):
#         return "<Tweet: {}>".format(self.text)
# def insert_example_users():
#     """Will get error if ran twice since data already exist"""
#     nick = User(id=1, name="nwdelafu")
#     elonmusk = User(id=2, name="elonmusk")
#     maakawest = User(id=3, name='maakawest')
#     DB.session.add(nick)  # adds nick User
#     DB.session.add(elonmusk)  # adds elon User
#     DB.session.add(maakawest)
#     DB.session.commit()  # commits all

# def insert_example_tweets():
#     tw1 = Tweet(id=1, text='send dogecoin to the moon', user_id=2, user='elonmusk')
#     tw2 = Tweet(id=2, text='BITCOIN to the moon', user_id=3, user='maakawest')
#     tw3 = Tweet(id=3, text='send TESLA to the moon!', user_id=2, user='elonmusk')
#     tw4 = Tweet(id=4, text='send maakawest to the moon', user_id=3, user='maakawest')
#     tw5 = Tweet(id=5, text='send Becca to the moon, and leave her there', user_id=3, user='maakawest')
#     tw6 = Tweet(id=6, text='send Maverick to the moon', user_id=1, user='nick')
#     DB.session.add(tw1)
#     DB.session.add(tw2)
#     DB.session.add(tw3)
#     DB.session.add(tw4)
#     DB.session.add(tw5)
#     DB.session.add(tw6)
#     DB.session.commit()
