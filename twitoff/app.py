"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, request
from .twitter import add_or_update_user
from .models import DB, User, Tweet, MIGRATE
from .predict import predict_user


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)
    MIGRATE.init_app(app, DB)

    # TODO - make rest of application

    @app.route('/')
    def root():
        # SQL equivalent = "SELECT * FROM user;"
        users = User.query.all()
        return render_template('base.html', title="Home", users=users)

    
    @app.route("/compare", methods=["POST"]) # method post allows us to grab stuff from the front end
    def compare():
        user0, user1 = sorted([request.values["user1"], request.values["user2"]])
        # Conditional that prevents the same user comparison
        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            hypo_tweet_text = request.values["tweet_text"] #tweet text is from the front end, we havent seen yet
            prediction = predict_user(user0, user1, hypo_tweet_text)
            message = "{} is more likely to be said by {} than {}".format(
                hypo_tweet_text, user1 if prediction else user0, user0 if prediction else user1
            )
        return render_template('prediction.html', title="prediction", message=message)

    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=""):
        name = name or request.values["user_name"] # this is grabbing a variable specified in the html documents
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} sucessfully added!".format(name)

            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error handling {}: {}".format(name, e)
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)


    @app.route("/update")
    def update():
        # add_or_update_user("elonmusk")
        users = User.query.all()
        for user in users:
            add_or_update_user(user.name)
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset Database")

    return app

# app.run(debug=True)










# """Main aopp/file routing for twitoff"""

# from flask import Flask, render_template
# def create_app():
#     app = Flask(__name__)

#     # TODO - make rest of application

#     # This brings us to our base route for our webapp
#     # An @ that goes before a function is a python decorator (given to us by flask)

#     @app.route('/')
#     def root():
#         return render_template('base.html', title="Home")

#     # @app.rpute('/reset') This could be used to make a /reset page


#     return app

# """Main app/routing file for Twitoff"""
# from os import getenv
# from flask import Flask, render_template
# from .models import DB, User, Tweet, insert_example_users, insert_example_tweets
# def create_app():
#     app = Flask(__name__)
#     app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     DB.init_app(app)
#     # TODO - make rest of application
#     @app.route('/')
#     def root():
#         insert_example_users()
#         # SQL equivalent = "SELECT * FROM user;"
#         users = User.query.all()
#         return render_template('base.html', title="Home", users=users)
#     return app
#     def root():
#         DB.drop_all()
#         DB.create_all()
#         insert_example_tweets()
#         tweets = Tweet.query.all()
#         return render_template('base.html', title="Home", tweets=tweets)

#     @app.route('/update')
#     def update():
#         insert_example_users()
#         return render_template("base.html", title="Home")

#     @app.route('/reset')
#     def reset():
#         DB.drop_all()
#         DB.create_all()
#         return render_template("base.html", title="Home")
#     return app