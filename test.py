import requests
import json
from pprint import pprint


def get_req(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"

    payload = json.dumps({
        "messages": [
            {
                "content": "You are a helpful assistant.",
                "role": "system"
            },
            {
                "content": prompt,
                "role": "user"
            }
        ],
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "stop": None,
        "stream": False,
        "temperature": 1,
        "top_p": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer sk-00555d8174554646a11276b58553a664'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


req = '''
Деловые мероприятия 2-ое полугодие 2024. 

Я знаю, что вы давно этого ждали!
Мы наконец составили список деловых мероприятий для второго полугодия 2024 года. 

Тематики:
◾️HR
◾️IT
◾️управление
◾️бизнес
◾️маркетинг/реклама/PR
◾️ИИ
◾️финансы

Забрать его можно в моем телеграм-боте.  (https://t.me/imaria_bot)
Вместе с мероприятиями вас ждет 🎁 – мини-урок на тему «6 способов позиционирования»

Я решила использовать своего бота как кладезь постов, полезной информации по личному бренду. Теперь там вас ждут: интересные кейсы, полезные материалы и эфиры с открытыми разборами. 

Это поможет вам изучить больше полезной информации и понимать, что именно ВЫ можете применить на практике!

*Если у вас уже есть переписка с ботом — сначала перезапустите его (инструкцию оставлю в комментариях)

**Если вы ещё не были в моем боте - запускайте и следуйте по инструкции внутри бота:)
'''
prompt = '''
Дай доброжелательный осмысленный комментарий от первого лица. Размер комментария должен быть равен шести словам. Максимум одному предложению.
Веди себя реалистично и позитивно. Не делай оценочных суждений.
'''
full_req = req + prompt
response = get_req(full_req)
pprint(response.text)
