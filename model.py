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
    'RqUID': '***',
    'Authorization': 'Basic ***'
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
