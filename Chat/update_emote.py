import requests
import json
import urllib.request
import os
from dotenv import load_dotenv

from emote import emote_dict

load_dotenv()

members = [
    {'name':'우왁굳', 'user_id': '49045679', 'user_login': 'woowakgood', 'profile':'ebc60c08-721b-4572-8f51-8be7136a0c96', 'color': 0x164532, 'offline': '1d94ad47-f32c-452e-8a28-07e73876bfe0', 'live': False, 'title': 'title'},
    {'name':'아이네', 'user_id': '702754423', 'user_login': 'vo_ine', 'profile':'ecd6ee59-9f18-4eec-b8f3-63cd2a9127a5', 'color': 0x8a2be2, 'offline': 'cba3d08e-a269-43ab-9448-2d9bf88751ee', 'live': False, 'title': 'title'},
    {'name':'징버거', 'user_id': '237570548', 'user_login': 'jingburger', 'profile':'330b695d-63ec-41cb-baca-a191a7bbc441', 'color': 0xf0a957, 'offline': 'a6d6432d-8cfb-41ee-92a8-8ff528307ca6', 'live': False, 'title': 'title'},
    {'name':'릴파', 'user_id': '169700336', 'user_login': 'lilpaaaaaa', 'profile':'3b5e6d73-8935-449f-902b-1b94a386e137', 'color': 0x000080, 'offline': 'd003b049-6435-4862-98c3-8acae4a59033', 'live': False, 'title': 'title'},
    {'name':'주르르', 'user_id': '203667951', 'user_login': 'cotton__123', 'profile':'919e1ba0-e13e-49ae-a660-181817e3970d', 'color': 0x800080, 'offline': 'aea85c64-5e28-4d15-81a1-db1a7a3cc1ec', 'live': False, 'title': 'title'},
    {'name':'고세구', 'user_id': '707328484', 'user_login': 'gosegugosegu', 'profile':'1e4cac72-a1cd-4f72-8ada-b2d10ac990d7', 'color': 0x467ec6, 'offline': '8bd8f49b-f1f7-460b-a35a-19a1800c71ee', 'live': False, 'title': 'title'},
    {'name':'비챤', 'user_id': '195641865', 'user_login': 'viichan6', 'profile':'d9db10b1-f7cf-44ce-942e-0ad8f1692813', 'color': 0x85ac20, 'offline': '0c205a38-8331-4bc0-8796-72e37c424584', 'live': False, 'title': 'title'},
]


for member in members:

    url = 'https://api.twitch.tv/helix/chat/emotes'


    headers = {
        'client-id' : os.getenv("twitch_client_id"),
        'Authorization' : os.getenv("twitch_app_access_token"),
    }

    params = {
        "broadcaster_id": str(member['user_id'])
    }

    response = requests.get(url, headers=headers, params=params)

    contents = json.loads(response.content)


    list = contents["data"]

    for i in list:

        if i['name'] not in emote_dict:
            print(f"\:{i['name']}:")
            try:
                if 'animated' in i['format']: # 움짤
                    url = i['images']['url_4x'].replace('static/', 'default/')
                    savelocation = f"./isedol_emoticon/temp/{i['name']}.gif"
                    urllib.request.urlretrieve(url, savelocation)

                else: # 이미지
                    url = i['images']['url_4x'].replace('static/', 'default/')
                    savelocation = f"./isedol_emoticon/temp/{i['name']}.png"
                    urllib.request.urlretrieve(url, savelocation)
            except:
                pass
    print()


'''
위에 한번 돌리고, 저장된 이미지들 디코서버에 추가 후, 터미널에 출력된거 복사해서 디코서버에 보내서 이모지id얻고, change에 넣고 돌린뒤 emote.py에 추가
'''