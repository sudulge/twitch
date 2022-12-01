from flask import Flask, request, abort
import requests
import json
import hmac
import hashlib
import random
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


TWITCH_MESSAGE_ID = 'Twitch-Eventsub-Message-Id'
TWITCH_MESSAGE_TIMESTAMP = 'Twitch-Eventsub-Message-Timestamp'
TWITCH_MESSAGE_SIGNATURE = 'Twitch-Eventsub-Message-Signature'
MESSAGE_TYPE = 'Twitch-Eventsub-Message-Type'

MESSAGE_TYPE_VERIFICATION = 'webhook_callback_verification'
MESSAGE_TYPE_NOTIFICATION = 'notification'
MESSAGE_TYPE_REVOCATION = 'revocation'


HMAC_PREFIX = 'sha256='


def getSecret():
    # TODO: Get your secret from secure storage. This is the secret you passed 
    # when you subscribed to the event.
    return '<your secret goes here>'

def getHmacMessage(request):
    return str(request.headers.get(TWITCH_MESSAGE_ID) + request.headers.get(TWITCH_MESSAGE_TIMESTAMP) + request.get_data().decode('utf-8')).encode("UTF-8")

def getHmac(secret, message):
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

# def verifyMessage(hmac, verifySignature):
#     return crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(verifySignature))

##########################################################################################

members = {
        "49045679": {'name':'우왁굳', 'user_id': '49045679', 'user_login': 'woowakgood', 'profile':'ebc60c08-721b-4572-8f51-8be7136a0c96', 'color': 0x164532, 'offline': '1d94ad47-f32c-452e-8a28-07e73876bfe0', 'live': False, 'title': 'title'},
        "702754423": {'name':'아이네', 'user_id': '702754423', 'user_login': 'vo_ine', 'profile':'ecd6ee59-9f18-4eec-b8f3-63cd2a9127a5', 'color': 0x8a2be2, 'offline': 'cba3d08e-a269-43ab-9448-2d9bf88751ee', 'live': False, 'title': 'title'},
        "237570548": {'name':'징버거', 'user_id': '237570548', 'user_login': 'jingburger', 'profile':'330b695d-63ec-41cb-baca-a191a7bbc441', 'color': 0xf0a957, 'offline': 'a6d6432d-8cfb-41ee-92a8-8ff528307ca6', 'live': False, 'title': 'title'},
        "169700336": {'name':'릴파', 'user_id': '169700336', 'user_login': 'lilpaaaaaa', 'profile':'3b5e6d73-8935-449f-902b-1b94a386e137', 'color': 0x000080, 'offline': 'e5f52835-cb99-4a07-bb58-aa777209895d', 'live': False, 'title': 'title'},
        "203667951": {'name':'주르르', 'user_id': '203667951', 'user_login': 'cotton__123', 'profile':'c90c5d02-5a9f-4906-a745-08ee8bf8ea18', 'color': 0x800080, 'offline': '92f19ffa-f0e2-49cd-9047-61754fe0f4ad', 'live': False, 'title': 'title'},
        "707328484": {'name':'고세구', 'user_id': '707328484', 'user_login': 'gosegugosegu', 'profile':'1e4cac72-a1cd-4f72-8ada-b2d10ac990d7', 'color': 0x467ec6, 'offline': '8bd8f49b-f1f7-460b-a35a-19a1800c71ee', 'live': False, 'title': 'title'},
        "195641865": {'name':'비챤', 'user_id': '195641865', 'user_login': 'viichan6', 'profile':'d9db10b1-f7cf-44ce-942e-0ad8f1692813', 'color': 0x85ac20, 'offline': '0c205a38-8331-4bc0-8796-72e37c424584', 'live': False, 'title': 'title'},
}

wh_url = os.getenv("discord_twitch_webhook_url")

wh_headers = {
    'Content-Type' : 'application/json',
}

def info(id: str):
    member = members[id]
    return member

def stream(member):
    url = 'https://api.twitch.tv/helix/streams'
    headers = {
    'client-id' : os.getenv("twitch_client_id"),
    'Authorization' : os.getenv("twitch_app_access_token"),
    }
    params = {'user_login': member['user_login']}
    response = requests.get(url, headers=headers, params=params)
    contents = json.loads(response.content)["data"][0]

    image = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{member['user_login']}-1499x843.jpg"
    thumbnail = f"https://static-cdn.jtvnw.net/jtv_user_pictures/{member['profile']}-profile_image-300x300.png"
    link = f"https://www.twitch.tv/{member['user_login']}"

    dic = {'name': member["name"], 'color': member["color"], 'title': contents["title"], 'content': contents["game_name"], 'thumbnail': thumbnail, 'image': image, 'link': link}

    return dic

def stream_embed(dic):
    data = {
        "username": f"{dic['name']} 뱅온",
        "embeds": [
            {
                "title" : dic['title'],
                "color" : dic['color'],
                "fields" : [
                    {
                        "name" : "컨텐츠",
                        "value": dic['content'],
                        "inline": True
                    },
                    {
                        "name" : "​",
                        "value": f"[보러가기]({dic['link']})"
                    }
                ],
                "thumbnail" : {"url": dic['thumbnail']},
                "image" : {"url": dic['image']}
            }
        ]
    }
    return data

def change(member):
    if member['live']:
        image = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{member['user_login']}-1499x843.jpg"
    else:
        image = f"https://static-cdn.jtvnw.net/jtv_user_pictures/{member['offline']}-channel_offline_image-1920x1080.png"
    thumbnail = f"https://static-cdn.jtvnw.net/jtv_user_pictures/{member['profile']}-profile_image-300x300.png"
    link = f"https://www.twitch.tv/{member['user_login']}"

    dic = {'name': member["name"], 'color': member["color"], 'before_title': member["title"], 'thumbnail': thumbnail, 'image': image, 'link': link}

    return dic

def change_embed(dic, after_title):
    data = {
        "username": f"{dic['name']} 뱅송 제목 변경",
        "embeds": [
            {
                "title" : after_title,
                "color" : dic['color'],
                "fields" : [
                    {
                        "name" : "변경 이전 제목",
                        "value": dic['before_title'],
                        "inline": False
                    },
                    {
                        "name" : "​",
                        "value": f"[보러가기]({dic['link']})"
                    }
                ],
                "thumbnail" : {"url": dic['thumbnail']},
                "image" : {"url": dic['image']}
            }
        ]
    }
    return data

##################################################################################

@app.route('/')
def hello():
    return 'go to eventsub'

@app.route('/eventsub', methods=['POST'])
def eventsub():
    secret = 'this is my secret'.encode("UTF-8")
    message = getHmacMessage(request)
    hmac_ = HMAC_PREFIX + getHmac(secret, message)

    if hmac_ == request.headers.get(TWITCH_MESSAGE_SIGNATURE):
        # print('signatures match')

        notification = request.get_json()
        member = info(notification["subscription"]["condition"]["broadcaster_user_id"])
        # print(request.headers) 
        # print(notification)

        # 알림
        if MESSAGE_TYPE_NOTIFICATION == request.headers.get(MESSAGE_TYPE):

            # 뱅온
            if notification["subscription"]["type"] == 'stream.online':
                dic = stream(member)
                data = stream_embed(dic)
                requests.post(url=wh_url, headers=wh_headers, json=data)
                member['live'] = True
                print(f'\n\n{member["name"]} 뱅온  {member["title"]}')
                return 'ok'

            # 방제 변경
            elif notification["subscription"]["type"] == 'channel.update':
                if notification["event"]["title"] != member["title"]:
                    dic = change(member)
                    data = change_embed(dic, notification["event"]["title"])
                    requests.post(url=wh_url, headers=wh_headers, json=data)
                    print(f'\n\n{member["name"]} 방제 변경 ')
                    print(f'{member["title"]}  ->  {notification["event"]["title"]}')
                    member["title"] = notification["event"]["title"]
                    return 'ok'
                else:
                    pass
            
            # 오뱅알
            elif notification["subscription"]["type"] == 'stream.offline':
                member['live'] = False
                return 'ok'

        # 구독 요청
        elif MESSAGE_TYPE_VERIFICATION == request.headers.get(MESSAGE_TYPE):
            print('\nsuccessfully make subscribe')
            return notification["challenge"]
        
        # 구독 폐지?
        elif MESSAGE_TYPE_REVOCATION == request.headers.get(MESSAGE_TYPE):
            print(f'{notification["subscription"]["type"]} notifications revoked!')
            print(f'reason: {notification["subscription"]["status"]}')
            print(f'condition: {json.dumps(notification["subscription"]["condition"], indent=4)}')
            print(204)
            return 'ok'

    else:
        print('403')
        abort(403)

    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)


#########################################
"""
모바일 디코 알림에서 확인하기 편하게 바꾸기 이전의 임베드 스타일
(디스코드 내에서 보기가 편함. )
# stream embed

    data = {
        "embeds": [
            {
                "title" : f"{dic['name']} 뱅온",
                "color" : dic['color'],
                "fields" : [
                    {
                        "name" : "방송 제목",
                        "value": dic['title'],
                        "inline": True
                    },
                    {
                        "name" : "컨텐츠",
                        "value": dic['content'],
                        "inline": True
                    },
                    {
                        "name" : "​",
                        "value": f"[보러가기]({dic['link']})"
                    }
                ],
                "thumbnail" : {"url": dic['thumbnail']},
                "image" : {"url": dic['image']}
            }
        ]
    }

# change embed

    data = {
        "embeds": [
            {
                "title" : f"{dic['name']} 뱅송 제목 변경",
                "color" : dic['color'],
                "fields" : [
                    {
                        "name" : "변경 이전 제목",
                        "value": dic['before_title'],
                        "inline": False
                    },
                    {
                        "name" : "변경 후 제목",
                        "value": after_title,
                        "inline": False
                    },
                    {
                        "name" : "​",
                        "value": f"[보러가기]({dic['link']})"
                    }
                ],
                "thumbnail" : {"url": dic['thumbnail']},
                "image" : {"url": dic['image']}
            }
        ]
    }
"""

