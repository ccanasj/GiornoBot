from .combat_manager import attack, defend, skill, skill_check
from random import randint
from time import time
from .stand_string import stats_to_string, effects_emojis


def bot_turn(bot, player, turn):
    skill_check(bot, turn)
    if randint(0, 100) <= 15 and not 'guard' in bot['status']:
        cadena = defend(bot)
    elif randint(0, 100) <= 40 and 'skill' in bot['actions']:
        cadena = skill(bot, player)
    else:
        cadena = attack(bot, player)
    return cadena


def player_turn(attacker, defender, turn, embed, text):
    stats_attacker = stats_to_string(attacker["stats"], attacker["type"])
    stats_defender = stats_to_string(defender["stats"], defender["type"])
    embed.description = f'<t:{round(time() + 30.0)}:R>'
    embed.set_author(name=f'Turno: #{turn} --- Turno de: {attacker["user"]["name"]}',
                     icon_url=attacker['user']['avatar'])
    embed.set_field_at(0, name=f'『 {attacker["name"]} 』', value=stats_attacker)
    embed.set_field_at(2, name=f'『 {defender["name"]} 』', value=stats_defender)
    embed.set_field_at(3, name=f'**Efectos:** {" - ".join([effects_emojis[status] for status in attacker["status"]])}',
                       value=text, inline=False)
    embed.set_thumbnail(url=attacker['user']['avatar'])
