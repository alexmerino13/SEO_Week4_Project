from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)

proxied = FlaskBehindProxy(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/menu")
def about():
    return render_template('menu.html', subtitle='Menu', text='This is a menu page')

@app.route('/RandomAnime')
def randAnime():
    try:

        rand = random.randint(1, 50000)
        suggest = kitsupy.get_info('anime', rand)['titles']['en']
        suggestRating = kitsupy.get_info('anime', rand)['averageRating']
        videoID = kitsupy.get_info('anime', rand)["youtubeVideoId"]
        if videoID == "":
            trailer = "No trailer available"
        else:
            trailer = "https://www.youtube.com/embed/" + videoID

        return render_template("randomAnime.html", anime="Anime: " + suggest,
                               rating="\nRating: " + suggestRating + "/100", trailer=trailer)
    except:
        return randAnime()




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
