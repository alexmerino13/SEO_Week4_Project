import json
import requests


def get_fact() -> tuple:
    url = 'https://asli-fun-fact-api.herokuapp.com/'
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    about = data["data"]["cat"]
    fact = data["data"]["fact"]
    return about, fact


def about(fact_data: tuple) -> str:
    if fact_data[0] == 'sea':
        return f'Did you know this about the {fact_data[0]}??'
    elif fact_data[0] == 'human':
        return f'Did you know this about {fact_data[0]}s??'
    elif fact_data[0] == 'auto':
        return f'Did you know this about {fact_data[0]}mobiles??'
    return f'Did you know this about {fact_data[0]}??'


def the_fact(fact_data: tuple) -> str:
    return f'{fact_data[1]}'


if __name__ == '__main__':
    fact = get_fact()
    print(about(fact))
    print(the_fact(fact))