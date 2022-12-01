import websockets
import asyncio
import re
import requests
from emote import emote_dict, members
import os
from dotenv import load_dotenv

load_dotenv()

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
            print('Server connect...')
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
            print('Server Disconnect...')
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