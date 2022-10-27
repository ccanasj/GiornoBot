from random import randint
from .stand_manager import apply_attributes


def attack(attacker, defender):
    hit = randint(1, 100)
    text = f'***{attacker["user"]["name"]}*** tu ataque **falló**'
    if hit <= attacker['stats']['accuracy']:
        power = attacker['stats']['power']
        if 'guard' in defender['status']:
            power -= round(power * defender['status'].pop('guard'))

        defender['stats']['hp'][-1] -= power
        text = f'¡**{attacker["user"]["name"]}** Acertaste tu ataque! **{defender["user"]["name"]}** perdio ' + \
            f'**{power}** ❤ de vida'
        check_hp(defender)

    return text

def defend(player):
    player['status']['guard'] = 0.3
    return f'***{player["user"]["name"]}***, te **defiendes** del proximo ataque'


def skill(attacker, defender):
    cadena = f'***{attacker["user"]["name"]}*** Usaste tu habilidad ***{attacker["skill"]["name"]}***\n'
    if attacker["skill"]['self']:
        for stat, value in attacker["skill"]['values'].items():
            if stat == 'hp':
                increase = round(defender['stats']['maxHP'] * (value / 100))
                defender['stats'][stat][-1] += increase
            else:
                increase = round(attacker['stats'][stat] * (value / 100))
                attacker['stats'][stat] += increase
            cadena += f'La **{stat}** aumento **{increase}** (*{value}%*)'
    else:
        for stat, value in attacker["skill"]['values'].items():
            if stat == 'hp':
                increase = round(defender['stats']['maxHP'] * (value / 100))
                defender['stats'][stat][-1] -= increase
            else:
                increase = round(attacker['stats'][stat] * (value / 100))
                defender['stats'][stat] -= increase
            cadena += f'La **{stat}** se redujo **{increase}** (*{value}%*)\n'
    check_hp(defender)
    attacker['actions'].remove('skill')
    return cadena


def check_hp(defender):
    if defender['stats']['hp'][-1] <= 0:
        defender['stats']['hp'].pop()

def set_stands(*players):
    for player in players:
        player['stats']['maxHP'] = player['stats']['hp'][0]
        player['actions'] = ['strike', 'guard']
        player['status'] = {}
        apply_attributes(player['stats'], player['attributes'])
        # greater_range = player['stats']['range'] if player['stats']['range'] > greater_range else greater_range


def skill_check(player, turn):
    if "skill" in player['actions']:
        return False
    elif player['stats']['activation'] <= turn:
        player['actions'].append('skill')
        player['stats']['activation'] += player['stats']['activation']
        return False
    return True

# def EfectosFinal(Jugador):
#     efecto = ''
#     if '☣' in Jugador['status']:
#         vidaPerdida = round(Jugador['Vida'][-1] * 0.2)
#         Jugador['Vida'][-1] -= vidaPerdida
#         Jugador['status']['☣'] -= 1
#         if Jugador['status']['☣'] <= 0:
#             Jugador['status'].pop('☣')
#         efecto = f'Perdiste **❤ {vidaPerdida}** por la infeccion'
#     return efecto

# def EfectosInicio(Jugador,turno):
#     if '⏱' in Jugador['status']:
#         Jugador['status']['⏱'] -= 1
#         if Jugador['status']['⏱'] <= 1:
#             Jugador['status'].pop('⏱')
#         return True
#     if '💗' in Jugador['status']:
#         if Jugador['status']['💗'] * 5 == turno:
#             Jugador['status']['💗'] += 1
#             Jugador['Vida'][0] += 100
#             Jugador['Rango'] += 5
#             Jugador['Fuerza'] += 20
#             Jugador['Precision'] += 5
#             Jugador['Velocidad'] += 5
#             return f'💗 Tu stand a llegado a la evolucion __{Jugador["status"]["💗"]}__'
#     return ''
