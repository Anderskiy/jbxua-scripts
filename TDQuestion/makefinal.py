import json
from copy import deepcopy

first = True
choicemode = False
titlemode = True

content = []

choices_t_o = {
    "controllerClass": "",
    "correct": True,
    "text": ""
}

choices_o = {
    "controllerClass": "",
    "text": ""
}

t_o = {
    "hasOutro": False,
    "x": False,
    "id": "",
    "text": "",
    "pic": False,
    "choices": [],
    "us": False,
    "hasIntro": False
       }  # Шаблон завдання

with open('basequestion.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    line = line.replace('\n', '')
    s = line.split(chr(9))
    if s[0].isdigit():  # Визначення рядка з номером завдання
        if first:  # Якщо перше завдання
            t = deepcopy(t_o)
            t["id"] = s[0]
            if s[2] == '1':  # Перевірка завдання на локальне запитання
                t["us"] = True
            first = False
            titlemode = True
        else:  # Для всіх інших завдань
            choicemode = False
            content.append(t)
            t = deepcopy(t_o)
            t["id"] = s[0]
            if s[2] == '1':  # Перевірка завдання на локальне запитання
                t["us"] = True
            choices = []
            titlemode = True

    elif s[0] == "Intro":
        t["hasIntro"] = True

    elif titlemode:  # Якщо рядок містить запитання завдання
        t["text"] = s[2]
        titlemode = False
        choicemode = True

    elif choicemode:  # Обробка варіантів відповіді
        if s[0] == "v":
            choice = deepcopy(choices_t_o)
            choice['text'] = s[2]
            t["choices"].append(choice)
        else:
            choice = deepcopy(choices_o)
            choice['text'] = s[2]
            t["choices"].append(choice)

content.append(t)

n = open('TDQuestion.jet', 'w', encoding='utf-8')
n.write(json.dumps({"episodeid": 1391, "content": content}, ensure_ascii=False, indent=2))
n.close()
