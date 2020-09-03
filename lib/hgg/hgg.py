import os
import requests
import json


API_KEY = os.getenv('DD_HGG_API_KEY', None)


def check_hgg_by_uuid(uuid):
    if API_KEY is None:
        return False
    uri = 'https://script.tftech.de/api/hgg.php?key={}&byUUID={}'.format(
        API_KEY, uuid)
    response = requests.get(uri)
    return json.loads(response.text)
