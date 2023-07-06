import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()

members = {
    "우왁굳": {'name':'우왁굳', 'user_id': '49045679', 'profile':'', 'number':0},
    "아이네": {'name':'아이네', 'user_id': '702754423', 'profile':'', 'number':0},
    "징버거": {'name':'징버거', 'user_id': '237570548', 'profile':'', 'number':0},
    "릴파 LILPA": {'name':'릴파', 'user_id': '169700336', 'profile':'', 'number':0},
    "주르르": {'name':'주르르', 'user_id': '203667951', 'profile':'', 'number':0},
    "고세구": {'name':'고세구', 'user_id': '707328484', 'profile':'', 'number':0},
    "비챤": {'name':'비챤', 'user_id': '195641865', 'profile':'', 'number':0},
}

for member in members:
    url = f"http://127.0.0.1:80/isedol/{members[member]['user_id']}"
    response = requests.get(url=url)
    contents = json.loads(response.content)

    members[member]['profile'] = contents['profile']

print(members)

cafe_url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=27842958&search.menuid=345&search.boardtype=L'
wh_url = os.getenv("discord_twitch_webhook_url")
headers = {
    'Content-Type' : 'application/json',
}

articleid_reg = re.compile("(?<=articleid=)[0-9]+")

def get_article_id():
    try:
        response = requests.get(cafe_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find_all('div', 'article-board m-tcol-c')[1]
        href = div.find('a')['href']
        name = div.find('td', 'td_name').text.strip()
        article_id = articleid_reg.search(href).group()
        return article_id, name
    except:
        pass

old_id, name = get_article_id()


while True:
    try:
        new_id, name = get_article_id()
        if new_id != old_id:
            old_id = new_id

            data = {
                "username": members[name]['name'],
                "avatar_url": f"https://static-cdn.jtvnw.net/jtv_user_pictures/{members[name]['profile']}-profile_image-300x300.png",
                "content": f"https://cafe.naver.moe/steamindiegame/{new_id}"
            }
            post = requests.post(url=wh_url, headers=headers, json=data)

    except:
        pass
    
    time.sleep(60)