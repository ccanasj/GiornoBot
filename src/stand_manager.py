from random import choice, choices, randint
from json import load
from api import get_name

with open('./src/Skills.json') as f:
    skills = load(f)

categories = {0: 'E', 1: 'D', 2: 'C', 3: 'B', 4: 'A', 5: 'S'}

types = ['Corto Alcance', 'Largo Alcance', 'Agil',
         'Multiple', 'Armadura', 'Evolución', 'Basico']

attributes_names = ['⚡ Velocidad', '🔪 Poder destructivo',
                    '💡 Potencial', '🎯 Precision', '🕛 Estamina', '🏹 Rango']

stars = [1, 2, 3]
stars_probability = [0.6, 0.3, 0.1]

stars_requiem = [2, 3]
stars_requiem_probability = [0.75, 0.25]

attributes = [0, 1, 2, 3, 4, 5]
attributes_probability = [0.16, 0.38, 0.3, 0.1, 0.05, 0.01]

attributes_requiem = [1, 2, 3, 4, 5]
attributes_requiem_probability = [0.1, 0.35, 0.3, 0.15, 0.1]

bosses = [{'name': 'Dio Brando', 'type': 0, 'attributes': [2, 1, 1, 2, 1, 2]},
          {'name': 'Kars', 'type': 6, 'attributes': [2, 3, 1, 1, 3, 3]},
          {'name': 'DIO', 'type': 0, 'attributes': [4, 4, 3, 3, 4, 2]},
          {'name': 'Yoshikage Kira', 'type': 1, 'attributes': [3, 3, 4, 1, 4, 4]},
          {'name': 'Diavolo', 'type': 6, 'attributes': [4, 4, 5, 5, 0, 0]},
          {'name': 'Enrico Pucci', 'type': 2, 'attributes': [5, 3, 4, 2, 4, 2]},
          {'name': 'Funny Valentine', 'type': 0, 'attributes': [4, 4, 4, 4, 4, 2]}]


def get_boss(part):
    boss = bosses[part - 1]
    velocity = 35 + (part * 2)
    hp = randint(1000, 1050) + (part * 200)
    power = randint(95, 100) + (part * 30)
    range = 10 + (part * 2)
    accuracy = 65 + (part * 3) + (boss['attributes'][3] * 5)
    stats = {'velocity': velocity, 'hp': [hp], 'power': power,
             'range': range, 'accuracy': accuracy, 'activation': 8 - boss['attributes'][4]}
    set_type(type, stats)
    boss['skill'] = get_skill(boss['attributes'][2])
    boss['stats'] = stats
    boss['star'] = 3
    return boss


async def generate_stand():
    name = await get_name()
    stand = {'name': name, 'level': [1, 0, 100]}
    type = randint(0, len(types) - 1)
    values = choices(population=attributes,
                     weights=attributes_probability, k=6)
    star = choices(population=stars, weights=stars_probability)[0]
    velocity = 25 + (star * 3)
    hp = randint(400, 600) + (star * 100)
    power = randint(70, 80) + (star * 10)
    range = 10 + (star * 2)
    accuracy = 60 + (star * 5) + (values[3] * 5)
    stats = {'velocity': velocity, 'hp': [hp], 'power': power,
             'range': range, 'accuracy': accuracy, 'activation': 8 - values[4]}
    set_type(type, stats)
    stand['skill'] = get_skill(values[2])
    stand['attributes'] = values
    stand['stats'] = stats
    stand['star'] = star
    stand['type'] = type
    return stand


async def generate_stand_requiem():
    name = f'{await get_name()} requiem'
    stand = {'name': name, 'level': [1, 0, 100]}
    type = randint(0, len(types) - 1)
    values = choices(population=attributes_requiem,
                     weights=attributes_requiem_probability, k=6)
    star = choices(population=stars_requiem,
                   weights=stars_requiem_probability)[0]
    velocity = 28 + (star * 3)
    hp = randint(500, 700) + (star * 100)
    power = randint(80, 90) + (star * 10)
    range = 13 + (star * 2)
    accuracy = 65 + (star * 2) + (values[3] * 5)
    stats = {'velocity': velocity, 'hp': [hp], 'power': power,
             'range': range, 'accuracy': accuracy, 'activation': 8 - values[4]}
    set_type(type, stats)
    stand['skill'] = get_skill(values[2])
    stand['attributes'] = values
    stand['stats'] = stats
    stand['star'] = star
    stand['type'] = type
    return stand


def set_type(type, stats):
    if type == 0:
        stats['hp'][0] = round(stats['hp'][0] * 1.2)
        stats['range'] -= 8
        stats['power'] = round(stats['power'] * 1.2)
        stats['accuracy'] += 3
    elif type == 1:
        stats['hp'][0] = round(stats['hp'][0] * 0.9)
        stats['range'] += 10
        stats['velocity'] += 5
        stats['power'] -= round(stats['power'] * 0.9)
        stats['accuracy'] -= 3
    elif type == 2:
        stats['velocity'] += 5
        stats['activation'] -= 1
    elif type == 3:
        hp = round(stats['hp'][0] / 5)
        stats['hp'] = [hp] * 4
        stats['accuracy'] += 3
        stats['range'] += 2
        stats['velocity'] += 2
    elif type == 4:
        hp = round(stats['hp'][0] * 0.7)
        shield = round(stats['hp'][0] * 0.2)
        stats['hp'] = [hp, shield]
        stats['range'] += 3
        stats['power'] = round(stats['power'] * 1.1)
        stats['accuracy'] += 3
        stats['velocity'] += 3
    elif type == 5:
        stats['hp'][0] = round(stats['hp'][0] * 0.6)
        stats['range'] -= 7
        stats['power'] -= round(stats['power'] * 0.7)
        stats['accuracy'] -= 5
        stats['velocity'] -= 6
    elif type == 6:
        stats['hp'][0] = round(stats['hp'][0] * 1.1)
        stats['range'] += 2
        stats['power'] = round(stats['power'] * 1.1)
        stats['accuracy'] += 2
        stats['velocity'] += 2


def get_skill(potential, old_skill = None):
    if not old_skill:
        skill = {**choice(skills)}
    else:
        copy = [*skills]
        copy.pop(old_skill['id'])
        skill = {**choice(copy)}

    skill['values'] = {k: (v + (v * potential))
                        for k, v in skill['values'].items()}
    return skill


def set_attributes(stand):
    min_attributes = [index for index, menor in enumerate(
        stand['attributes']) if menor < 4]
    if min_attributes:
        key = choice(min_attributes)
        stand['attributes'][key] += 1
        response = {'old_attribute': categories[stand['attributes'][key] - 1],
                    'new_attribute': categories[stand['attributes'][key]],
                    'attribute_name': attributes_names[key]}
        if key == 2:
            skill = skills[stand['skill']['id']]
            stand['skill']['values'] = {
                k: (v + (v * stand['attributes'][key])) for k, v in skill['values'].items()}
        elif key == 3:
            stand['stats']['accuracy'] += 5
        elif key == 4:
            stand['stats']['activation'] -= 1
        return response
    return None


def apply_attributes(stats, attributes):
    stats['power'] += round(stats['power'] * (attributes[1] / 10))
    stats['velocity'] += round(stats['velocity'] * (attributes[0] / 10))
    stats['range'] += round(stats['range'] * (attributes[5] / 10))
