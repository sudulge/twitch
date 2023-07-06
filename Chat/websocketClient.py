import websockets
import asyncio
import re
import requests
from emote import emote_dict
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

members = {
    "49045679": {'name':'우왁굳', 'user_id': '49045679', 'user_login': 'woowakgood', 'profile':'', 'offline': '', 'color': 0x164532, 'live': False, 'title': 'title'},
    "702754423": {'name':'아이네', 'user_id': '702754423', 'user_login': 'vo_ine', 'profile':'', 'offline': '', 'color': 0x8a2be2, 'live': False, 'title': 'title'},
    "237570548": {'name':'징버거', 'user_id': '237570548', 'user_login': 'jingburger', 'profile':'', 'offline': '', 'color': 0xf0a957, 'live': False, 'title': 'title'},
    "169700336": {'name':'릴파', 'user_id': '169700336', 'user_login': 'lilpaaaaaa', 'profile':'', 'offline': '', 'color': 0x000080, 'live': False, 'title': 'title'},
    "203667951": {'name':'주르르', 'user_id': '203667951', 'user_login': 'cotton__123', 'profile':'', 'offline': '', 'color': 0x800080, 'live': False, 'title': 'title'},
    "707328484": {'name':'고세구', 'user_id': '707328484', 'user_login': 'gosegugosegu', 'profile':'', 'offline': '', 'color': 0x467ec6, 'live': False, 'title': 'title'},
    "195641865": {'name':'비챤', 'user_id': '195641865', 'user_login': 'viichan6', 'profile':'', 'offline': '', 'color': 0x85ac20, 'live': False, 'title': 'title'},
}

for member in members:
    url = f"http://127.0.0.1:5000/isedol/{member}"
    response = requests.get(url=url)
    contents = json.loads(response.content)

    members[member]['profile'] = contents['profile']
    members[member]['offline'] = contents['offline']

ws_url = 'ws://irc-ws.chat.twitch.tv:80'
wh_url = os.getenv("discord_twitch_webhook_url")
headers = {
    'Content-Type' : 'application/json',
}

room_reg = re.compile("(?<=room-id=)[0-9]+")
user_reg = re.compile("(?<=user-id=)[0-9]+")
chat1_reg = re.compile("(?<=PRIVMSG\s#).+")
chat2_reg = re.compile("(?<=\s:).+")


async def connect():
    
    async for websocket in websockets.connect(ws_url):
        try:
            print(f'{datetime.now()} Server connect...')
            await websocket.send('CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands')
            await websocket.send(f'PASS oauth:{os.getenv("twitch_user_access_token").replace("Bearer ","")}')
            await websocket.send(f'NICK {os.getenv("twitch_id")}')
            await websocket.send('JOIN #woowakgood,#vo_ine,#jingburger,#lilpaaaaaa,#cotton__123,#gosegugosegu,#viichan6')

            while True:
                data = await websocket.recv()

                if 'PING :tmi.twitch.tv' in str(data):
                    await websocket.send('PONG :tmi.twitch.tv')

                try:
                    user_id = user_reg.search(data).group()
                    room_id = room_reg.search(data).group()
                    chat = chat2_reg.search(chat1_reg.search(data).group()).group()

                    if members[user_id]:
                        for i in emote_dict:
                            emote_reg = re.compile(f"{i}\s")
                            chat = emote_reg.sub(f"{emote_dict[i]} " , chat)
                        await sendwh(user_id, room_id, chat)

                except:
                    pass

        except websockets.ConnectionClosed:
            print(f'{datetime.now()} Server Disconnect...')
            continue

async def sendwh(user_id, room_id, chat):
    try:
        if user_id == room_id:
            data = {
                "username": members[user_id]['name'],
                "avatar_url": f"https://static-cdn.jtvnw.net/jtv_user_pictures/{members[user_id]['profile']}-profile_image-300x300.png",
                "content": chat
            }
        else:
            data = {
                "username": f"{members[user_id]['name']}  ->  {members[room_id]['name']}",
                "avatar_url": f"https://static-cdn.jtvnw.net/jtv_user_pictures/{members[user_id]['profile']}-profile_image-300x300.png",
                "content": chat
            }

        requests.post(url=wh_url, headers=headers, json=data)
    except:
        pass


asyncio.run(connect())