import requests
from bs4 import BeautifulSoup
import re
import time
import os
from dotenv import load_dotenv

load_dotenv()

members = {
    "우왁굳": {'name':'우왁굳', 'profile':'ebc60c08-721b-4572-8f51-8be7136a0c96', 'number':0},
    "아이네": {'name':'아이네', 'profile':'ecd6ee59-9f18-4eec-b8f3-63cd2a9127a5', 'number':0},
    "징버거": {'name':'징버거', 'profile':'330b695d-63ec-41cb-baca-a191a7bbc441', 'number':0},
    "릴파 LILPA": {'name':'릴파', 'profile':'3b5e6d73-8935-449f-902b-1b94a386e137', 'number':0},
    "주르르": {'name':'주르르', 'profile':'919e1ba0-e13e-49ae-a660-181817e3970d', 'number':0},
    "고세구": {'name':'고세구', 'profile':'1e4cac72-a1cd-4f72-8ada-b2d10ac990d7', 'number':0},
    "비챤": {'name':'비챤', 'profile':'d9db10b1-f7cf-44ce-942e-0ad8f1692813', 'number':0},
}

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