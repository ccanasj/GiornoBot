from .stand_manager import apply_attributes


attributes_values = {   0: '¦ ㅤ ㅤ ㅤ ㅤ ㅤ - E',
                        1: '¦ ▮ ㅤ ㅤ ㅤ ㅤ - D ',
                        2: '¦ ▮ ▮ ㅤ ㅤ ㅤ - C',
                        3: '¦ ▮ ▮ ▮ ㅤ ㅤ - B',
                        4: '¦ ▮ ▮ ▮ ▮ ㅤ - A',
                        5: '¦ ▮ ▮ ▮ ▮ ▮ - S'}

effects_emojis = {'guard': '🛡','Time Stop': '⏱', 'Vampirism': '🩸',
                 'Revive': '🧬', 'Infected': '☣'}

activation_emoji = ('🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙')

stats_emojis = {'velocity': '⚡', 'hp': '❤', 'power': '🔪',
                'range': '🏹', 'accuracy': '🎯', 'activation': '🕛'}


def stand_to_string(stand):
    apply_attributes(stand['stats'], stand['attributes'])
    attributes = attributes_to_string(stand['attributes'])
    stats = stats_to_string(stand['stats'], stand['type'])
    return stats, attributes


def attributes_to_string(attributes):
    string_attributes = f'**⚡ {attributes_values[attributes[0]]}\n🔪 {attributes_values[attributes[1]]}\n💡 {attributes_values[attributes[2]]}\n🎯 {attributes_values[attributes[3]]}\n{activation_emoji[attributes[4]]} {attributes_values[attributes[4]]}\n🏹 {attributes_values[attributes[5]]}**'
    return string_attributes


def skill_to_string(skill):
    string_skill = f'Habilidad de **{"estado" if skill["self"] else "ataque"}**\n'
    string_skill += '\n'.join(
        [f'{stats_emojis[stat]} | **{value}**%' for stat, value in skill['values'].items()])
    return string_skill


def stats_to_string(stats, type):
    hp = f'❤ Vida - {stats["hp"][0]}'
    if type == 3:
        hp = '💕 Vida - ' + ' | '.join([str(valor) for valor in stats["hp"]])
    elif type == 4:
        hp = f'💖 Vida - {stats["hp"][0]} - 🛡️ {stats["hp"][1] if len(stats["hp"]) == 2 else "0"}'
    string_stats = f'**{hp} \n🔪 Fuerza - {stats["power"]}\n🏹 Rango - {stats["range"]} m\n🎯 Precision - {stats["accuracy"]}%\n⚡ Velocidad - {stats["velocity"]}\n{activation_emoji[stats["activation"] % 10]} Activacion - {stats["activation"]} Turnos**'
    return string_stats

