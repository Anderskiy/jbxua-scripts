import json
from copy import deepcopy

items = []
item = {
    "difficulty": 1,
    "correct": bool,
    "text": str
}

first = True
itemmode = False

t_o = {
    "x": False,
    "id": 0,
    "text": "",
    "choices": [],
    "us": False
}

content = []

with open('base.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    print("line: ", line)
    s = line.split(chr(9))  # Разбиваем строку на элементы
    print("s: ", s)
    if s[0].isdigit() and int(s[0]) > 50000:  # Проверяем, является ли первый элемент числом
        if not first:
            content.append(t)  # Добавляем предыдущий элемент в список
        else:
            first = False

        t = deepcopy(t_o)  # Создаем полную копию объекта
        t["id"] = int(s[0])
        t["us"] = s[3] == '1'
        t["x"] = s[6] == '1'
        itemmode = False
    elif itemmode:
        itm = deepcopy(item)  # Создаем полную копию объекта
        itm["difficulty"] = int(s[4])
        itm["correct"] = s[5] == "v"
        itm["text"] = s[6]
        t["choices"].append(itm)
    else:
        t["text"] = s[6]
        itemmode = True

if t:  # Добавляем последний элемент, если он существует
    content.append(t)

n = open('TDFinalRound.jet', 'w', encoding='utf-8')
n.write(json.dumps({"episodeid": 1390, "content": content}, ensure_ascii=False, indent=2))
n.close()

n = open('TDFinalRoundTech.jet', 'w', encoding='utf-8')
n.write(json.dumps({"episodeid": 1390, "content": content}, ensure_ascii=False, indent=2))
n.close()
