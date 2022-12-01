import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 사용자 액세스 토큰  크롬 주소창에 직접 입력. # chat read, chat edit 스코프
# url = https://id.twitch.tv/oauth2/authorize
#       ?response_type=token
#       &client_id=<your client id>
#       &redirect_uri=http://localhost:5000
#       &scope=chat%3Aread+chat%3Aedit

# 앱 액세스 토큰 발급 .post params
# url = 'https://id.twitch.tv/oauth2/token'
# params = {
#     'client_id' : os.getenv("twitch_client_id"),
#     'client_secret' : os.getenv("twitch_client_secret"),
#     'grant_type' : 'client_credentials',
# }

# 토큰 제거 .post data
# url = 'https://id.twitch.tv/oauth2/revoke'
# data = {
#     'client_id' : os.getenv("twitch_client_id"),
#     'token' : '',
# }


# 토큰 유효성 검사 .get headers
url = 'https://id.twitch.tv/oauth2/validate'
headers = {
    'Authorization' : os.getenv("twitch_app_access_token"),
}

response = requests.get(url, headers=headers)
contents = response.text

print(contents)