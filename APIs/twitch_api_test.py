import requests
import json
from pprint import pprint
from datetime import datetime, timedelta, date, time
import webbrowser
import re
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

members = [
        {'name':'우왁굳', 'user_id': '49045679', 'user_login': 'woowakgood', 'profile':'ebc60c08-721b-4572-8f51-8be7136a0c96', 'color': 0x164532, 'offline': '1d94ad47-f32c-452e-8a28-07e73876bfe0', 'live': False, 'title': ''},
        {'name':'아이네', 'user_id': '702754423', 'user_login': 'vo_ine', 'profile':'ecd6ee59-9f18-4eec-b8f3-63cd2a9127a5', 'color': 0x8a2be2, 'offline': 'cba3d08e-a269-43ab-9448-2d9bf88751ee', 'live': False, 'title': ''},
        {'name':'징버거', 'user_id': '237570548', 'user_login': 'jingburger', 'profile':'330b695d-63ec-41cb-baca-a191a7bbc441', 'color': 0xf0a957, 'offline': 'a6d6432d-8cfb-41ee-92a8-8ff528307ca6', 'live': False, 'title': ''},
        {'name':'릴파', 'user_id': '169700336', 'user_login': 'lilpaaaaaa', 'profile':'3b5e6d73-8935-449f-902b-1b94a386e137', 'color': 0x000080, 'offline': 'e5f52835-cb99-4a07-bb58-aa777209895d', 'live': False, 'title': ''},
        {'name':'주르르', 'user_id': '203667951', 'user_login': 'cotton__123', 'profile':'c90c5d02-5a9f-4906-a745-08ee8bf8ea18', 'color': 0x800080, 'offline': '92f19ffa-f0e2-49cd-9047-61754fe0f4ad', 'live': False, 'title': ''},
        {'name':'고세구', 'user_id': '707328484', 'user_login': 'gosegugosegu', 'profile':'1e4cac72-a1cd-4f72-8ada-b2d10ac990d7', 'color': 0x467ec6, 'offline': '8bd8f49b-f1f7-460b-a35a-19a1800c71ee', 'live': False, 'title': ''},
        {'name':'비챤', 'user_id': '195641865', 'user_login': 'viichan6', 'profile':'d9db10b1-f7cf-44ce-942e-0ad8f1692813', 'color': 0x85ac20, 'offline': '0c205a38-8331-4bc0-8796-72e37c424584', 'live': False, 'title': ''},
    #   {'name':'천양', 'user_id': '132782743', 'user_login': 'chunyangkr', 'profile':'f49375d7-f953-40c8-bb16-949c26d34121', 'color': 0xacfef9, 'live': False, 'title': ''},
]



# Get Channel Information
# https://api.twitch.tv/helix/channels GET
# broadcaster_id 

# Search Channels
# https://api.twitch.tv/helix/search/channels GET
# query

# Get Streams
# https://api.twitch.tv/helix/streams GET
# user_id or user_login

# Get Users
# https://api.twitch.tv/helix/users GET
# id, login

# Get Videos
# https://api.twitch.tv/helix/videos GET
# user_id

# Get Clips
# https://api.twitch.tv/helix/clips GET
# broadcaster_id

# Get Predictions   216051440 hhs0888
# https://api.twitch.tv/helix/predictions GET
# broadcaster_id

# GET emotes
# https://api.twitch.tv/helix/chat/emotes GET
# broadcaster_id



url = 'https://api.twitch.tv/helix/channels'

headers = {
    'client-id' : os.getenv("twitch_client_id"),
    'Authorization' : os.getenv("twitch_app_access_token"),
}

params = {
    # "broadcaster_id": "49045679",
    # "started_at": "2022-11-18T20:00:00+09:00",
    # "ended_at": "2022-11-18T20:08:12+09:00",
    # "first": "100"
    "broadcaster_id": "237570548"
}

response = requests.get(url, headers=headers, params=params)
contents = json.loads(response.content)

pprint(contents)

# for i in contents['data']:
#     print(f"{i['title']}: {i['view_count']} {i['url']}")


# 이모티콘 뽑기용
# list = contents["data"]
# count = 0
# count_ = 0
# for i in list:
#     count +=1
#     try:
#         if (len(i['format']) > 1):
#             url = dict(i['images'].items())['url_4x']
#             url = str(url).replace('static/', 'default/')
#             savelocation = f"./image/viichan6/{i['name']}.gif"
#             urllib.request.urlretrieve(url, savelocation)
#             count_ += 1

#         else:
#             url = dict(i['images'].items())['url_4x']
#             url = str(url).replace('static/', 'default/')
#             savelocation = f"./image/viichan6/{i['name']}.png"
#             urllib.request.urlretrieve(url, savelocation)
#             count_ += 1
#     except:
#         print(count, count_)
#         pass

# print(count)
# print(count_)