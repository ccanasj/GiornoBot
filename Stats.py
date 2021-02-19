import random as rd
import asyncio
import json

valor ={0:'¦ ㅤ ㅤ ㅤ ㅤ ㅤ - E',
        1:'¦ ▮ ㅤ ㅤ ㅤ ㅤ - D ',
        2:'¦ ▮ ▮ ㅤ ㅤ ㅤ - C',
        3:'¦ ▮ ▮ ▮ ㅤ ㅤ - B',
        4:'¦ ▮ ▮ ▮ ▮ ㅤ - A',
        5:'¦ ▮ ▮ ▮ ▮ ▮ - S',}

Valores = [0,1,2,3,4,5]
Probabilidades = [0.2,0.4,0.25,0.1,0.045,0.005]

s = 'Velocidad_Vida_Fuerza_Rango_Precision_Duracion'
formato = s.split('_')
with open('Ability.json','r') as f:
    file = json.load(f)

async def Estadisticas():
    ability = rd.choice(file)
    values = rd.choices(population = Valores,weights = Probabilidades,k = 6)
    velocidad = rd.randint(30,50)
    PorncentajeVel = round((velocidad + (velocidad * (values[0] / 10))))
    HP = rd.randint(250,350)
    Poder = rd.randint(70,85)
    PorncentajePoder = round((Poder + (Poder * (values[1] / 10))))
    Rango = rd.randint(50,80)
    PorncentajeRango = round((Rango + (Rango * (values[5] / 10))))
    Precision = 65 + (values[3] * 5)
    if ability['limitation']:
        ability['value'][0] +=  values[2]
    else:
        for x in range(len(ability['value'])):
            ability['value'][x] += values[2]
    stats = {'Velocidad':PorncentajeVel,'Vida':HP,'Fuerza':PorncentajePoder,
    'Rango':PorncentajeRango,'Precision':Precision,'Duracion':values[4],'Habilidad': ability}
    return values,stats

async def Atributos(atributos):
    cadena = f'**Vel {valor[atributos[0]]}\nPod {valor[atributos[1]]}\nPot {valor[atributos[2]]}\nPre {valor[atributos[3]]}\nDur {valor[atributos[4]]}\nRan {valor[atributos[5]]}**'
    return cadena

async def StringStats(stats):
    Estadistica = f'**⚡ - Velocidad - {stats[formato[0]]} \n❤  - Vida - {stats[formato[1]]} \n🔪 - Fuerza - {stats[formato[2]]} \n🏹 - Rango - {stats[formato[3]]} m\n🎯 - Precision - {stats[formato[4]]}%\n⏱ - Duracion - {stats[formato[5]]} Turnos**'
    return Estadistica

async def Damage(atacante,victima,nombre):
    tiro = rd.randint(0,100)
    cadena = 'Nothing'
    victoria = False
    if tiro <= atacante['Precision']:
        victima['Vida'] -= atacante['Fuerza']
        if victima['Vida'] <= 0:
            cadena = f'!{nombre} a Ganado!'
            victoria = True
        else:
            cadena = f'{nombre} ¡Acertaste tu ataque! Le quitaste **{atacante["Fuerza"]}** ❤ de vida'
    else:
        cadena = f'{nombre} Tu ataque a fallado'
    return victoria,cadena
    
async def ActivateAbility(stats,nombre):
    ability = stats['Habilidad']
    stats['Habilidad']['amount'] -= 1
    cadena = 'None'
    if ability['limitation']:
        stat = stats[ability['stat'][0]]
        limitation = stats[ability['stat'][1]]
        values = ability['value']
        increase = round(stat + (stat * (values[0] / 10)))
        decrease = round(limitation - (limitation * (values[1] / 10)))
        stats[ability['stat'][0]] = increase
        stats[ability['stat'][1]] = decrease
        cadena = f'{nombre} has usado **『{ability["name"]}』**\n Tu **{ability["stat"][0]}** aumento a: **{str(increase)}**\nTu **{ability["stat"][1]}** se redujo a: **{str(decrease)}**'
    else:
        cadena = f'{nombre} has usado **『{ability["name"]}』**\n'
        for x in range(len(ability['value'])):
            stat = stats[ability['stat'][x]]
            value = ability['value'][x]
            increase = round(stat + (stat * (value/ 10)))
            stats[ability['stat'][x]] = increase    
            cadena += f'Tu **{ability["stat"][x]}** aumento a: **{str(increase)}** \n'
    return cadena
