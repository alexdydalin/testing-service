import requests
import json



condition = ''' Текст ниже  написан на языке Ghirkin в код на Java \n '''

# Получение токена
def get_token():
  url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

  payload = 'scope=GIGACHAT_API_PERS'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': 'a3f6728e-58a7-4e8b-a9a2-a051721570f1',
    'Authorization': 'Basic ODZlMTljZTgtNjIxOC00MDJjLTkxOWYtNTliZWMzMzk2ZmEwOjk3YmMwZmM0LTIxNTktNDdiMS05MWI3LTlkODM3NWZkZDAyNA=='
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  token_data = response.json()
  token = token_data['access_token']

  return token


# Получение результата генерации
def get_generate_result(token, ghirkin_text):
  authorization = 'Bearer ' + token
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat",
    "messages": [
      {
        "role": "user",
        "content": condition + ghirkin_text
      }
    ],
    "stream": False,
    "update_interval": 0
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': authorization
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  ans = json.loads(response.text)
  ans_message = ans["choices"][0]["message"]["content"]
  ans_message = ans_message.split("```")

  return (ans_message[1])





















# Authorization Key
# ODZlMTljZTgtNjIxOC00MDJjLTkxOWYtNTliZWMzMzk2ZmEwOjk3YmMwZmM0LTIxNTktNDdiMS05MWI3LTlkODM3NWZkZDAyNA==
#
# Client Secret
# 97bc0fc4-2159-47b1-91b7-9d8375fdd024
#
# Client ID
# 86e19ce8-6218-402c-919f-59bec3396fa0