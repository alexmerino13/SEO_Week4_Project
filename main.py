from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from nytAPI import nyt
import kitsupy
import random
import requests
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
    random_url = nyt.get_random_url() # random story url generated
    stories = nyt.get_response(random_url) # list of random stories and urls
    randStory = nyt.return_random_story(stories) # single tuple with url at index 0 and abstract at index 1
    popularstory = nyt.get_popular_stories() # single tuple with Popular story url at index 0 and abstract at index 1
    # randStory and popularstory use two different endpoints on the NYT API. That explains the odd styling for my render_template
    # The "Generate New Stories" button resets the webpage and allows for two new stories to be generated
    # on very rare (extremely rare) occassions - the randStory will return without an abstract, simply is a function of how the data is entered in the NYT API
    ## no cause for concern^^ just should reset and regenerate stories
    return render_template("randomArticle.html", rand_url="Random Story url: " +randStory[0], 
                            rand_story="Abstract: " + randStory[1], pop_url="Popular Story url: " + popularstory[0], 
                            pop_story="Abstract: " + popularstory[1])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")