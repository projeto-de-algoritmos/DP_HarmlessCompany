import json
import os
import random
from junk.junk import Junk

def junk_list():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    file = "junk.json"
    file_path = os.path.join(file)
    absolute_path = os.path.abspath(file_path)

    with open(absolute_path, "r+") as a:
        items = json.load(a)

    # Selecionar aleatoriamente essa quantidade x de itens
    random_items= random.sample(items, k=10)

    junk_items = []
    for item in random_items:
        name = item['Scrap Name']
        value = item['Value Range'] 
        weight = item['Weight']
        junk_items.append(Junk(name, value, weight))

    return junk_items