from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import hashlib
import webbrowser

url = input("Twicth Tracker URL 입력: ")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
meta = soup.find_all('meta')[3]['content']

id = url.split("/")[3]
streamcord = url.split("/")[-1]
startime = meta.split(" - ")[0].split("on ")[1]
d = datetime.strptime(startime, "%Y-%m-%d %H:%M:%S")
e = timedelta(hours=9)
f = d + e
timestamp = int(f.timestamp())

string = f"{id}_{streamcord}_{timestamp}"
sha = hashlib.new('sha1')
sha.update(string.encode())
hash = sha.hexdigest()[:20]

subdomains = ["d1m7jfoe9zdc1j", "d2nvs31859zcd8", "d3vd9lfkzbru3h", "dgeft87wbj63p"]
for i in subdomains:
    webbrowser.open(f"https://{i}.cloudfront.net/{hash}_{string}/chunked/index-dvr.m3u8")