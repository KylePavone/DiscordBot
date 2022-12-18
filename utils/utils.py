import requests
import json


def get_req():
    response = requests.get('https://media.wired.co.uk/photos/60c8730fa81eb7f50b44037e/16:9/w_3332,h_1874,c_limit/1521-WIRED-Cat.jpeg').url
    return response




def test_tube(query: str):
    api_url = "https://www.googleapis.com/youtube/v3/search"
    google_api_key = 'AIzaSyArLUetwsI5eKwExxsl0W9ma_CYLd136NA'
    params = [
        f'q={query}',
        f'key={google_api_key}',
        'part=snippet',
        'type=video',
        'maxResults=10'
    ]
    pars = "&".join(params)
    query_url = f'{api_url}?{pars}'
    response = requests.get(query_url)
    # video_id = json.loads(response.text)
    # video_id['items'][0]['id']['videoId']
    return response.text


print(test_tube('angular'))
