import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()

members = [
    {'name':'우왁굳', 'user_id': '49045679', 'cafe_key': 'Iep9BEdfIxd759MU7JgtSg', 'color': 0x164532, 'profile':'', 'lastArticle_id':0},
    {'name':'아이네', 'user_id': '702754423', 'cafe_key': 'Lp-S_8ZQuLCK03pDpod-7Q', 'color': 0x8a2be2, 'profile':'', 'lastArticle_id':0},
    {'name':'징버거', 'user_id': '237570548', 'cafe_key': '8g_F8kj48MSqBeVnVAhnCw', 'color': 0xf0a957, 'profile':'', 'lastArticle_id':0},
    {'name':'릴파', 'user_id': '169700336', 'cafe_key': 'ANjFuUREskKRC7DcGwAXNA', 'color': 0x000080, 'profile':'', 'lastArticle_id':0},
    {'name':'주르르', 'user_id': '203667951', 'cafe_key': 'ri0vjEn1-XpglkwfwSDuBw', 'color': 0x800080, 'profile':'', 'lastArticle_id':0},
    {'name':'고세구', 'user_id': '707328484', 'cafe_key': 'kvYmWvSHP9_wnnbRX4nGXg', 'color': 0x467ec6, 'profile':'', 'lastArticle_id':0},
    {'name':'비챤', 'user_id': '195641865', 'cafe_key': '6Wj7By3k4NnbeXohIaIltQ', 'color': 0x85ac20, 'profile':'', 'lastArticle_id':0},
]

wh_url = os.getenv("discord_twitch_webhook_url")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
cookies = {
    "NID_SES": os.getenv("nid_ses"),
    "NID_AUT": os.getenv("nid_aut")
    }


def getLastArticle(cafe_key):
    url = f"https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberNetworkArticleListV1?search.cafeId=27842958&search.memberKey={cafe_key}"
    response = requests.get(url=url, headers=headers, cookies=cookies)
    articleList = json.loads(response.content)['message']['result']['articleList']
    lastArticle = articleList[0]
    return lastArticle


# 프로필 이미지 가져오기, 마지막 글 id 넣어주기
for member in members:
    url = f"http://127.0.0.1:5000/isedol/{member['user_id']}"
    response = requests.get(url=url)
    contents = json.loads(response.content)
    member['profile'] = contents['profile']

    lastArticle = getLastArticle(member['cafe_key'])
    lastArticle_id = lastArticle['articleid']
    member['lastArticle_id'] = lastArticle_id
    print(f"{member['name']}: {lastArticle['subject']}")


while True:
    try:
        for member in members:
            lastArticle = getLastArticle(member['cafe_key'])
            lastArticle_id = lastArticle['articleid']

            if lastArticle_id != member['lastArticle_id']:
                member['lastArticle_id'] = lastArticle_id

                url = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/27842958/articles/{lastArticle_id}'
                response = requests.get(url=url, headers=headers, cookies=cookies)
                soup = BeautifulSoup(json.loads(response.content)['result']['article']['contentHtml'], 'html.parser')
                
                if soup.find('img'):
                    if soup.find('img')['src'].startswith('https://cafeptthumb'):
                        img_url = soup.find('img')['src']
                    else:
                        img_url = None
                else:
                    img_url = None

                spans = soup.find_all('span')
                content = ''
                for span in spans:
                    content += f"{span.text}\n"

                data = {
                    "username": member['name'],
                    "avatar_url": f"https://static-cdn.jtvnw.net/jtv_user_pictures/{member['profile']}-profile_image-300x300.png",
                    "embeds": [
                        {
                            "author": {
                                "name": lastArticle['clubMenu']['menuname']
                            },
                            "title": lastArticle['subject'],
                            "url": f"https://cafe.naver.com/steamindiegame/{lastArticle_id}",
                            "color": member['color'],
                            "image": {"url": img_url},
                            "fields": [
                                {
                                    "name" : "",
                                    "value": content
                                }
                            ]
                        }
                    ],
                }
                post = requests.post(url=wh_url, headers={'Content-Type' : 'application/json'}, json=data)
    except:
        pass

    time.sleep(60)