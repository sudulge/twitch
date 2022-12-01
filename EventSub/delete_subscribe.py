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
}

params = {"id": "ff525fbd-3261-4c59-85df-ad3a7eccedc4"}


response = requests.delete(url, headers=headers, params=params)

pprint(response) # 204 success

