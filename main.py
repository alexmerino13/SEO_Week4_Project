from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from nytAPI import nyt
import requests
import kitsupy
import os

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

        # suggestImg = kitsupy.get_info('anime', rand)['posterImage']['tiny']

        return render_template("randomAnime.html", anime="Anime: " + suggest,
                               rating="\nRating: " + suggestRating + "/100", trailer=trailer)
    except:
        return randAnime()


@app.route('/Joke')
def Joke():
    url = "https://backend-omega-seven.vercel.app/api/getjoke"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    setup = response.json()[0]['question']
    punchLine = response.json()[0]['punchline']
    return render_template("Joke.html", setup=setup, punchLine=punchLine)


@app.route('/read')
def read():
    random_url = nyt.get_random_url()
    stories = nyt.get_response(random_url)
    randStory = nyt.return_random_story(stories)
    popular_story = nyt.get_popular_stories()
    info = nyt.display_stories(popular_story, randStory)
    return render_template("randomArticle.html", stories=randStory, popStory=popular_story)




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")