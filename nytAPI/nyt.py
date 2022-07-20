import requests
import json
import os
import random
import sqlalchemy as db
import pandas as pd

list_of_news_desk_values = ["Adventure Sports", "Arts & Leisure", "Arts","Automobiles","Blogs","Books","Booming","Business Day","Business","Cars","Circuits","Classifieds","Connecticut","Crosswords & Games","Culture","DealBook","Dining","Editorial","Education","Energy","Entrepreneurs","Environment","Escapes","Fashion & Style","Fashion","Favorites","Financial","Flight","Food","Foreign","Generations","Giving","Global Home","Health & Fitness","Health","Home & Garden","Home","Jobs","Key","Letters","Long Island","Magazine","Market Place","Media","Men's Health","Metro","Metropolitan","Movies","Museums","National","Nesting","Obits","Obituaries","Obituary","OpEd","Opinion","Outlook","Personal Investing","Personal Tech","Play","Politics","Regionals","Retail","Retirement","Science","Small Business","Society","Sports","Style","Sunday Business","Sunday Review","Sunday Styles","T Magazine","T Style","Technology","Teens","Television","The Arts","The Business of Green","The City Desk","The City","The Marathon","The Millennium","The Natural World","The Upshot","The Weekend","The Year in Pictures","Theater","Then & Now","Thursday Styles","Times Topics","Travel","U.S.","Universal","Upshot","UrbanEye","Vacation","Washington","Wealth","Weather","Week in Review","Week","Weekend","Westchester","Wireless Living","Women's Health","Working","Workplace","World","Your Money"]

api_key = os.environ.get("API_KEY")

base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=news_desk:({})&api-key={}"

def did_user_like() -> str:
    """
    To be run in order to keep track of stories
    that have been read by the user,
    and will return whether they like the story
    or not.
    """
    answer = input("Did either of these stories interest you?\ny/n:\n")
    
    # this code relies on the fact that the random "popular" story will be displayed as the "first" story and the random story is the second

    if answer is "y":
        question2 = input("Which story did you like?\nInput '1' for first story, '2' for the second, and '3' if you liked both:\n")
        if question2 is "1":
            print("Thank you for the input!")
            answer = "y1"
        elif question2 is "2":
            print("Thank you for the input!")
            answer = "y2"
        elif question2 is "3":
            print("Thank you for the input!")
            answer = "y3"
        else:
            print("Oops! Wrong input! Please try again!")
            did_user_like()
    elif answer is "n":
        print("We will do better with suggestions!")
        answer = "n"
    else:
        did_user_like()
    
    return answer


def get_random_url() -> str:
    """
    Gets a random news topic from the list of desk values,
    as provided by the NYT Article Search API.
    """
    global list_of_news_desk_values, api_key, base_url
    random_index = random.randint(1, len(list_of_news_desk_values)-1)
    news_desk_fq = list_of_news_desk_values[random_index].replace(" ", "")
    return base_url.format(news_desk_fq, api_key)
    

def get_response(url: str) -> dict:
    """
    Takes a url as a string,
    makes a call to the specified section of the NYT API,
    returns a json file dict.
    """
    answer = {}
    response = requests.get(url)
    if response.status_code != 200:
        get_response(get_random_url())


    def determine_story_validity(res) -> bool:
        """
        To be run in the get_response() func;
        will determine if the story returned is readable
        """
        big_dict = res.json()
        if 'response' not in big_dict.keys():
            return False
        doc_list = big_dict["response"]["docs"]
        if len(doc_list) == 0:
            return False
        return True


    while determine_story_validity(response) == False:
        response = requests.get(get_random_url())
        determine_story_validity(response)
    

    def parse_json(d: dict) -> None:
        """
        Function designed to parse the json file
        in order to return desired information.
        """
        counter = 1
        desired = d["response"]["docs"]
        for item in desired:
            info_list = []
            webURL = item['web_url']
            snippet = item['snippet']
            info_list.append(webURL)
            info_list.append(snippet)
            answer[counter] = info_list
            counter += 1
    
    parse_json(response.json())

    return answer
    

def return_random_story(d: dict) -> tuple:
    """
    Returns the abstract and web url for a random story
    that was chosen from the large dictionary of stories
    that is returned from get_response().
    """
    if len(d.keys()) == 0:
        url = get_random_url()
        res = get_response(url)
        return_random_story(res)
    else: 
        random_story = random.randint(1, max(d.keys()))
        story_info = d[random_story]
        return story_info[0], story_info[1]


def get_popular_stories() -> tuple:
    link = 'https://api.nytimes.com/svc/mostpopular/v2/viewed/{}.json?api-key={}'
    stories = []
    response = requests.get(link.format('30', api_key))
    res = response.json()
    list_of_dicts = res['results']
    for item in list_of_dicts:
        url = item['url']
        abstract = item['abstract']
        stories.append((url, abstract))
    return stories[random.randint(0, len(stories) - 1)]


def generated_story_info(popular_story: tuple, random_story: tuple) -> None:
    """
    Takes the stories that the user generates and adds them to a database.
    This also records whether the user enjoyed the articles/topics.
    """
    ret = {
        "Popular": [popular_story[0], popular_story[1]],
        "Random": [random_story[0], random_story[1]]
    }
    ans = did_user_like()
    if ans == "y1":
        ret["Popular"].append("y")
        ret["Random"].append("n")
    elif ans == "y2":
        ret["Popular"].append("n")
        ret["Random"].append("y")
    elif ans == "y3":
        ret["Popular"].append("y")
        ret["Random"].append("y")
    elif ans == "n":
        ret["Popular"].append("n")
        ret["Random"].append("n")
    
    story_tbl = pd.DataFrame.from_dict(ret, orient='index', columns=["Story URL", "Story Snippet", "Did user like? y/n"])

    engine = db.create_engine('sqlite:///Stories.db')
    story_tbl.to_sql('Stories', con=engine, if_exists='replace', index=False)
    
    # you can uncomment this to see what the db would look like
    # print(story_tbl)

    # A query to the db
    # q = engine.execute('SELECT * FROM Stories')


def display_stories(pop: tuple, rand: tuple) -> str:
    """
    Displays generated stories and necessary information about the stories.
    """
    return f'First story:\n\n\tStory url: {pop[0]}\n\tAbstract: {pop[1]}\n\nSecond story:\n\n\tStory url: {rand[0]}\n\tAbstract: {rand[1]}\n'


def read():
    """
    All together now...
    
    This is mostly for documentation to see how everything comes together
    """
    # random story url
    random_url = get_random_url()

    # making the request and getting a dictionary of stories
    stories = get_response(random_url)

    # parsing and returning a random story
    random_story = return_random_story(stories)

    # getting a random popular New York Times story from the last 30 days
    popular_story = get_popular_stories()

    # displaying the two stories to the user
    print(display_stories(popular_story, random_story))

    # Asks if user liked the stories, adding necessary info to a db
    generated_story_info(popular_story, random_story)
    

if __name__ == '__main__':
    # randurl = get_random_url()
    # stories = get_response(randurl)
    read()
    # print(stories)
    # print(stories[])