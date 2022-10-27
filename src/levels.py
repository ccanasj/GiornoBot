from random import choices, randint

stats = [("hp", 5, '❤'), ("power", 2, '🔪'),
         ("range", 1, '🏹'), ("velocity", 1, '⚡')]

stats_odds = [0.3, 0.3, 0.2, 0.2]


def experience(level,name, min_exp, max_exp):
    exp = (level[0] ** 2) + randint(min_exp, max_exp)
    level[1] += exp
    query = {'$set': {'stand.level': level}}
    text = f'Ganaste **{exp}** <a:Exp:840278760678096927>'
    if level[1] >= level[2]:
        level[0] += 1
        level[1] -= level[2]
        level[2] += round(level[2] * 0.15)
        stat, value, emoji = choices(population=stats, weights=stats_odds)[0]
        query['$set']['stand.level'] = level
        if stat == 'hp':
            query['$inc'] = {'stand.stats.hp.$[]': value}
        else:
            query['$inc'] = {f'stand.stats.{stat}': value}
        text += f'\n¡***{name}*** subio a nivel **{level[0]}**!\n Tu **{emoji} {stat}** aumento **+ {value}** punto/s'
    return text, query
