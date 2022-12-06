from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import hashlib
import os
import re

twitchtracker_reg = re.compile("^https?://twitchtracker.com/[a-zA-Z0-9-]+/streams/[0-9]+")
streamscharts_reg = re.compile("^https?://streamscharts.com/channels/[a-zA-Z0-9-]+/streams/[0-9]+")
time_reg = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}")

while True:
    url = input("\nURL을 입력해주세요 (트위치트래커 or 스트림차트): ").strip()
    if twitchtracker_reg.match(url):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        meta = soup.find_all('meta')[3]['content']

        userid = url.split("/")[3]
        streamid = url.split("/")[-1]
        startime = meta.split(" - ")[0].split("on ")[1]

        break
    elif streamscharts_reg.match(url):
        userid = url.split("/")[4]
        streamid = url.split("/")[-1]
        while True:
            startime = input("방송 시작 시간을 입력해주세요. YYYY-mm-dd HH:MM:SS : ").strip()
            if time_reg.match(startime):
                break
            else:
                print("올바른 시간 형식으로 입력해주세요")
        break

    else:
        print("잘못된 URL입니다. 다시 입력해주세요.")

d = datetime.strptime(startime, "%Y-%m-%d %H:%M:%S")
kst = timedelta(hours=9)
time = d + kst

timestamp = int(time.timestamp())
timestamp2 = timestamp+1
timestamp3 = timestamp-1

subdomains = ["d3vd9lfkzbru3h", "d1m7jfoe9zdc1j", "d2nvs31859zcd8", "dgeft87wbj63p"]

def printurl(time):
    string = f"{userid}_{streamid}_{time}"
    sha = hashlib.new('sha1')
    sha.update(string.encode())
    hash = sha.hexdigest()[:20]
    for i in subdomains:
        print(f"https://{i}.cloudfront.net/{hash}_{string}/chunked/index-dvr.m3u8\n")

print("기본")
printurl(timestamp)
print("+1초\n")
printurl(timestamp2)
print("-1초\n")
printurl(timestamp3)
os.system('pause')