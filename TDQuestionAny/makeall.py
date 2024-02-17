import asyncio
import json
from copy import deepcopy

first = True
choicemode = False
titlemode = False
sectionmode = {"mode": ""}

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
    "id": 0,
    "text": "",
    "pic": False,
    "choices": [],
    "us": False,
    "hasIntro": False
       }  # Шаблон завдання

content = []
t = {}

with open('base.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

async def makefile(episode: int, name: str, cont: list):
    n = open(f'TDQuestion{name}.jet', 'w', encoding='utf-8')
    n.write(json.dumps({"episodeid": episode, "content": cont}, ensure_ascii=False, indent=2))
    global content
    content.clear()
    global first
    first = True
    n.close()

for line in lines:
    line = line.replace('\n', '')
    line = line.replace("'", '’')
    line = line.replace('"', '”')
    s = line.split(chr(9))  # Розбиваємо рядок на елементи
    print("s: ", s)

    if s[0] == 'TDQuestionBomb':
        sectionmode["mode"] = "bomb"
        continue

    elif s[0] == "TDQuestionHat":
        content.append(t)
        asyncio.run(makefile(episode=1393, name="Bomb", cont=content))
        sectionmode["mode"] = "hat"
        choicemode = False
        continue

    elif s[0] == "TDQuestionWig":
        content.append(t)
        asyncio.run(makefile(episode=1392, name="Hat", cont=content))
        sectionmode["mode"] = "wig"
        choicemode = False
        continue

    elif s[0] == "TDQuestionKnife":
        content.append(t)
        asyncio.run(makefile(episode=1389, name="Wig", cont=content))
        sectionmode["mode"] = "knife"
        choicemode = False
        continue

    elif s[0] == "TDQuestionGhost":
        content.append(t)
        asyncio.run(makefile(episode=1394, name="Knife", cont=content))
        sectionmode["mode"] = "ghost"
        choicemode = False
        continue

    elif s[0] == "TDQuestionMadness":
        content.append(t)
        asyncio.run(makefile(episode=1396, name="Ghost", cont=content))
        sectionmode["mode"] = "madness"
        choicemode = False
        continue

    if s[0] == "озвучка": continue

    if s[0].isdigit():  # Визначення рядка з номером завдання
        if first:  # Якщо перше завдання
            t = deepcopy(t_o)
            t["id"] = int(s[0])
            if s[1] == '1':  # Перевірка завдання на локальне запитання
                t["us"] = True
            first = False
            titlemode = True
        else:  # Для всіх інших завдань
            choicemode = False
            content.append(t)
            t = deepcopy(t_o)
            t["id"] = int(s[0])
            if s[1] == '1':  # Перевірка завдання на локальне запитання
                t["us"] = True
            choices = []
            titlemode = True

    elif s[0] == "Intro":  # Якщо рядок містить інтро
        t["hasIntro"] = True

    elif titlemode:  # Якщо рядок містить запитання завдання
        if sectionmode["mode"] == "bomb" or sectionmode["mode"] == "knife" or sectionmode["mode"] == "ghost" or sectionmode["mode"] == "madness":
            t["text"] = "[EventName=HOST/AltHost]" + s[2]
        else:
            t["text"] = s[2]
        titlemode = False
        choicemode = True

    elif choicemode:  # Обробка варіантів відповіді
        if s[0] == "v":
            choice = deepcopy(choices_t_o)
            if sectionmode["mode"] == "bomb":
                choice['controllerClass'] = s[2]
            else:
                choice['text'] = s[2]
            t["choices"].append(choice)
        else:
            choice = deepcopy(choices_o)
            if sectionmode["mode"] == "bomb":
                choice['controllerClass'] = s[2]
            else:
                choice['text'] = s[2]
            t["choices"].append(choice)


content.append(t)
asyncio.run(makefile(episode=1395, name="Madness", cont=content))
