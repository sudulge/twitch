import requests
import json
from pprint import pprint
from datetime import datetime, timedelta, date, time
import os
from dotenv import load_dotenv

load_dotenv()


url = ' https://api.twitch.tv/helix/eventsub/subscriptions'

headers = {
    'client-id' : os.getenv("twitch_client_id"),
    'Authorization' : os.getenv("twitch_app_access_token"),
    'Content-Type' : 'application/json'
}

params = {
    "type" : "stream.online",
    "version" : "1",
    "condition" : {"broadcaster_user_id" : "195641865"},
    "transport" : {
        "method" : "webhook",
        "callback" : os.getenv("eventsub_callback_url"),
        "secret" : 'this is my secret'
    }
}

response = requests.post(url, headers=headers, data = json.dumps(params))
contents = json.loads(response.content)

pprint(contents)

'''
49045679 왁
702754423 아
237570548 징
169700336 릴
203667951 주
707328484 고
195641865 비
'''