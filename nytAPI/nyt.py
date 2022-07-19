import requests
import json
import os
import random
from apiInfo import list_of_news_desk_values, api_key, base_url


# I thought of using this like a way to store info in a database
# perhaps could be useful to have previous info on whether they liked the story or not.
def did_user_like() -> bool:
    """
    To be run in order to keep track of stories
    that have been read by the user,
    and will return whether they like the story
    or not.
    """
    answer = input("Did any of these stories interest you?\ny/n:\n")
    
    if answer is "y":
        print("Thank you for your input!")
        return True
    elif answer is "n":
        print("We will do better with suggestions!")
        return False
    # I was thinking of creating some sort of database
    # to store generated stories and whether the user
    # enjoyed the stories in the database.
    # Then we can filter out stories that they do not like.
    else:
        did_user_like() # will modularize


def get_random_url() -> str:
    """
    Gets a random news topic from the list of desk values,
    as provided by the NYT Article Search API.
    """
    global list_of_news_desk_values, api_key, base_url
    random_index = random.randint(0, len(list_of_news_desk_values))
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
    print(response.status_code)
    if response.status_code != 200:
        get_response(get_random_url())


    def determine_story_validity() -> bool: # needs improvement
        """
        To be run in the get_response() func;
        will determine if the story returned is readable
        """
        big_dict = response.json() # pause
        doc_list = big_dict["response"]["docs"]
        if len(doc_list) == 0:
            return False
        return True


    if determine_story_validity() is False:
        get_response(get_random_url())
    

    def parse_json() -> None:
        """
        Function designed to parse the json file
        in order to return desired information.
        """
        counter = 1
        big_dict = response.json()
        desired = big_dict["response"]["docs"]
        for item in desired:
            info_list = []
            webURL = item['web_url']
            abstract = item['abstract']
            info_list.append(webURL)
            info_list.append(abstract)
            answer[counter] = info_list
            counter += 1
        
    parse_json()

    return answer 
    

# to be continued...


if __name__ == '__main__':
    # print(get_random_url())
    random_url = get_random_url()
    print(random_url)
    print(get_response(random_url))
    print(did_user_like())
    print(get_random_url())
