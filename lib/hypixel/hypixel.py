import os
import requests
import json

API_KEY = os.getenv('DD_HYPIXEL_API_KEY', None)


def getplayer_by_name(name):
    if API_KEY is None:
        return False
    uri = 'https://api.hypixel.net/player?key={}&name={}'.format(API_KEY, name)
    response = requests.get(uri)
    return json.loads(response.text)


def getguild_by_playeruuid(uuid):
    if API_KEY is None:
        return False
    uri = 'https://api.hypixel.net/guild?key={}&player={}'.format(
        API_KEY, uuid)
    response = requests.get(uri)
    return json.loads(response.text)
