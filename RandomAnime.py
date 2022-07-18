import random
import kitsupy
from flask import Flask, request, render_template

# def getGerne(animeID):
#     print(animeID)
#     jikan = Jikan()
#     suggestedGenre = []
#     for items in jikan.anime(animeID)['genres']:
#         suggestedGenre.append(items['name'])
#     return suggestedGenre
app = Flask(__name__)


@app.route('/')
def randzAnime():
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
        return randzAnime()


# def animeSearch(anime):
#     return kitsupy.search('anime', anime)


if __name__ == '__main__':
    # print("Generating random anime...")
    # print(randzAnime())
    app.run(debug=True)
