import requests
import json
from pprint import pprint
from datetime import datetime, timedelta, date, time
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()


url = 'https://api.twitch.tv/helix/videos'

headers = {
    'client-id' : os.getenv("twitch_client_id"),
    'Authorization' : os.getenv("twitch_app_access_token"),
}

params = {}

member = input("\n\n\n멤버를 입력해주세요 [ENTER]직접입력 [0]왁 [1]아 [2]징 [3]릴 [4]주 [5]고 [6]비 ")
member_list = [49045679, 702754423, 237570548, 169700336, 203667951, 707328484, 195641865] #왁아징릴주고비

while True:
    if member == '':
        try:
            params["id"] = int(input("다시보기 id를 입력해 주세요 "))
            response = requests.get(url, headers=headers, params=params)
            contents = json.loads(response.content)
            if not contents["data"]:
                continue
            break
        except:
            continue
    else:
        params["user_id"] = member_list[int(member)]
        response = requests.get(url, headers=headers, params=params)
        contents = json.loads(response.content)
        del params["user_id"]
        params["id"] = contents["data"][0]["id"]

        response = requests.get(url, headers=headers, params=params)
        contents = json.loads(response.content)
        break


title = contents["data"][0]['title']
start_time = datetime.fromisoformat(contents["data"][0]['created_at'][:-1]) + timedelta(hours=9)
up_time = contents["data"][0]['duration']
if 'h' in up_time:
    up = datetime.strptime(up_time, "%Hh%Mm%Ss").time()
else:
    up = datetime.strptime(up_time, "%Mm%Ss").time()
end_time = start_time + timedelta(hours=up.hour, minutes=up.minute, seconds=up.second)


print(f"\n방송 제목: {title} | 뱅온: {start_time} | 뱅종: {end_time} | 업타임: {up_time}")

while True:
    option = input("\n옵션을 입력해 주세요. [Enter] 시간 -> 방송시간 [1] 방송시간 -> 시간 ")

    if option == '':
        while True:
            target_input = input("\n시간을 입력해 주세요. 형식 [HH] [MM] [SS] ")

            try:
                target_time = datetime.strptime(target_input, "%H %M %S").time()
            except:
                print("\n올바른 형식으로 입력해 주세요")
                continue

            if target_time < start_time.time() : #찾고자 하는 시간이 방송 시작 시간보다 작을경우 예) 21시 시작 03시 찾기
                target_datetime = datetime.combine(start_time.date()+timedelta(days=1), target_time)
            else:
                target_datetime = datetime.combine(start_time.date(), target_time)

            if target_datetime > end_time:
                print("\n방송 중인 시간을 입력해 주세요")
                continue


            d = datetime.strptime(str(target_datetime - start_time), '%H:%M:%S').time()
            print(f"\n{target_datetime.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}는 방송시간 <{d}>입니다.")
            print(f"\nhttps://www.twitch.tv/videos/{params['id']}?t={d.strftime('%Hh%Mm%Ss')}")
            break
        
        
    elif option == '1':
        while True:
            stream_input = input("\n방송시간을 입력해 주세요. 형식 [HH] [MM] [SS] ")

            try:
                stream_time = datetime.strptime(stream_input, "%H %M %S").time()
            except:
                print("\n올바른 형식으로 입력해 주세요")
                continue

            if stream_time > up: 
                print("\n업타임 내의 시간을 입력해 주세요")
                continue


            target_datetime = start_time + timedelta(hours=stream_time.hour, minutes=stream_time.minute, seconds=stream_time.second)
            print(f"\n방송시간 <{stream_time}>은 {target_datetime.strftime('%Y년 %m월 %d일 %H시 %M분 %S초 입니다')}")
            print(f"\nhttps://www.twitch.tv/videos/{params['id']}?t={stream_time.strftime('%Hh%Mm%Ss')}")
            break


    else:
        print('\n엔터키 or 1을 입력해 주세요')
        continue
    
    break


while True:
    a = input("링크로 이동?")
    if a == '':
        path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(path).open(f"\nhttps://www.twitch.tv/videos/{params['id']}?t={d.strftime('%Hh%Mm%Ss')}")
    else:
        quit()