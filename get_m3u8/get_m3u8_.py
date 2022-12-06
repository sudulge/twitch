from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import hashlib
import webbrowser

# url = input("Twicth Tracker URL 입력: ")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

list = {0:"woowakgood",
        1:"vo_ine",
        2:"jingburger",
        3:"lilpaaaaaa",
        4:"cotton__123",
        5:"gosegugosegu",
        6:"viichan6",
        7:None}

while True:
    # streamer = int(input("스트리머를 선택해주세요\n[0]우왁굳 [1]아이네 [2]징버거 [3]릴파 [4]주르르 [5]고세구 [6]비챤 [7]직접선택"))
    streamer = 0
    url = f"https://twitchtracker.com/{list[streamer]}/streams"
    break
    # else:
    #     print("올바른 입력을 해주세요")

print(url)
response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
meta = soup.find_all('a')
# ass = meta.find_all('a')
print(meta)
# id = url.split("/")[3]
# streamcord = url.split("/")[-1]
# startime = meta.split(" - ")[0].split("on ")[1]
# d = datetime.strptime(startime, "%Y-%m-%d %H:%M:%S")
# e = timedelta(hours=9)
# f = d + e
# timestamp = int(f.timestamp())

# string = f"{id}_{streamcord}_{timestamp}"
# sha = hashlib.new('sha1')
# sha.update(string.encode())
# hash = sha.hexdigest()[:20]

# subdomains = ["d1m7jfoe9zdc1j", "d2nvs31859zcd8", "d3vd9lfkzbru3h", "dgeft87wbj63p"]
# for i in subdomains:
#     webbrowser.open(f"https://{i}.cloudfront.net/{hash}_{id}_{streamcord}_{timestamp}/chunked/index-dvr.m3u8")

