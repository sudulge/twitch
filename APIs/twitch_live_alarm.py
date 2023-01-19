# 10초마다 뱅온, 뱅송제목변경 체크하는 프로그램

import requests
import json
import time
import random
from pprint import pprint
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import hashlib

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

headers = {
    'client-id' : os.getenv("twitch_client_id"),
    'Authorization' : os.getenv("twitch_app_access_token")
}

wh_url = os.getenv("discord_twitch_webhook_url")

wh_headers = {
    'Content-Type' : 'application/json',
}


# 처음 켜질 때 한번 실행
for member in members:
    url = 'https://api.twitch.tv/helix/streams'
    params = {'user_login': member['user_login']}
    response = requests.get(url, headers=headers, params=params)
    contents = json.loads(response.content)      # 방송이 안켜져 있으면 ["data"][0]에서 list index out of range 에러가 나기때문에 try문 안에서 읽어줘야함.

    try:
        if contents["data"][0]["type"] == 'live':
            member['live'] = True
    except:
        pass
    
    url = 'https://api.twitch.tv/helix/channels'
    params = {'broadcaster_id':  member['user_id']}
    response = requests.get(url, headers=headers, params=params)
    contents = json.loads(response.content)["data"][0]

    member['title'] = contents["title"]

    print(f"{member['name']}: {str(member['live']).ljust(5,' ')} {member['title']}")

#############################################################################################################

def getm3u8(contents):
    startime = str(contents["data"][0]["started_at"]).replace("T", " ").replace("Z", "")
    d = datetime.strptime(startime, "%Y-%m-%d %H:%M:%S")
    e = timedelta(hours=9)
    f = d + e
    timestamp = int(f.timestamp())
    t = f.strftime("%Y_%m_%d_%H_%M_%S")
    streamid = contents["data"][0]["id"]
    userid = contents["data"][0]["user_login"]

    string = f"{userid}_{streamid}_{timestamp}"
    sha = hashlib.new('sha1')
    sha.update(string.encode())
    hash = sha.hexdigest()[:20]

    m3u8 = f"https://d3vd9lfkzbru3h.cloudfront.net/{hash}_{string}/chunked/index-dvr.m3u8"
    return m3u8, t

def stream(member, contents):
    m3u8, t = getm3u8(contents)
    image = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{member['user_login']}-1499x843.jpg?t={t}"
    thumbnail = f"https://static-cdn.jtvnw.net/jtv_user_pictures/{member['profile']}-profile_image-300x300.png"
    link = f"https://www.twitch.tv/{member['user_login']}"

    dic = {'name': member["name"], 'color': member["color"], 'title': contents["data"][0]["title"], 'content': contents["data"][0]["game_name"], 'thumbnail': thumbnail, 'image': image, 'link': link, 'm3u8': m3u8}

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
                        "inline": False
                    },
                    {
                        "name" : "​",
                        "value": f"[보러가기]({dic['link']})",
                        "inline": True
                    },
                    {
                        "name" : "​",
                        "value": f"[m3u8]({dic['m3u8']})",
                        "inline": True
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
        image = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{member['user_login']}-1499x843.jpg" + str(random.randint(1, 999999))
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

###########################################################################################

while True:
    try:
        for member in members:
            url = 'https://api.twitch.tv/helix/streams'
            params = {'user_login': member['user_login']}
            response = requests.get(url, headers=headers, params=params)
            contents = json.loads(response.content)

            try:
                # 방송 켜져있고 멤버 live가 False 일 때
                if contents["data"][0]["type"] == 'live' and member['live'] == False:
                    dic = stream(member, contents)
                    data = stream_embed(dic)
                    post = requests.post(url=wh_url, headers=wh_headers, json=data)
                    member['live'] = True

                # 방송 켜져있고 멤버 live가 True 일 때
                else:
                    pass

            except:
                # 방송 꺼져있고 멤버 live가 True 일 때
                if member['live'] == True:
                    member['live'] = False

                # 방송 꺼져있고 멤버 live가 False 일 때
                else:
                    pass
            
            url = 'https://api.twitch.tv/helix/channels'
            params = {"broadcaster_id":  member['user_id']}
            response = requests.get(url, headers=headers, params=params)
            contents = json.loads(response.content)["data"][0]

            if contents["title"] != member['title']:
                dic = change(member)
                data = change_embed(dic, contents["title"])
                member["title"] = contents["title"]
                post = requests.post(url=wh_url, headers=wh_headers, json=data)
            else:
                pass

    except Exception as e:
        print(e)
        pass

    time.sleep(10)