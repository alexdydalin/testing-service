import os
from os import abort, remove
from flask import Flask, request, render_template, send_file, redirect, url_for
import requests
import json
import random

app = Flask(__name__)

condition = ''' Текст ниже  написан на языке описания алгоритвов Ghirkin, переведи его в код на Java с помощью  Cucamber \n '''

@app.route('/' , methods=['POST', 'GET'])
def index():
    bucket_dir = 'bucket'

    # Удаляем все файлы в папке bucket
    for filename in os.listdir(bucket_dir):
        file_path = os.path.join(bucket_dir, filename)
        try:
            os.remove(file_path)
            print(f'Файл "{file_path}" успешно удален.')
        except OSError as e:
            print(f'Ошибка при удалении файла: {e}')
    return render_template('index.html')


@app.route('/help', methods=['POST', 'GET'])
def help():
    return render_template('help.html')

@app.route('/history', methods=['POST', 'GET'])
def history():
    return render_template('history.html')


@app.route('/loading', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':
        # Получаем данные из формы
        data = request.form.get('text_input')
        req = condition + str(data)
        #print(req)
        token = get_token()
        java_code = get_generate_result(token, req)

        random_number = random.randint(1, 99999)
        file_path = 'generated_code.txt'
        new_filename = f"bucket/{file_path.split('.')[0]}_{random_number}.{file_path.split('.')[1]}"
        try:
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(str(java_code))
            print(f'Файл "{new_filename}" успешно создан.')
        except Exception as e:
            print(f'Ошибка при создании файла: {e}')

        try:
            return send_file(new_filename, as_attachment=True)
        except FileNotFoundError:
            return redirect(url_for('index'))

        #print(java_code)
        #return java_code
    return render_template('loading.html')

def remove_comment_lines(lines):
    cleaned_lines = []
    for line in lines:
        if not line.startswith('//'):
            cleaned_lines.append(line)
    return cleaned_lines

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
    print(ans_message)
    return (ans_message[1])



if __name__ == '__main__':
    app.run(debug=True)

