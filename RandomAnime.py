import kitsupy
import requests
from ranimegen.animegen import RandomAnime


async def randzAnime():
    generator = RandomAnime()
    suggestion = generator.suggestanime()
    return suggestion


def animeSearch():
    return kitsupy.search('anime', 'naruto')


if __name__ == '__main__':
    print(randzAnime())