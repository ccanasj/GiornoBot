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

ValoresRequiem = [1,2,3,4,5]
ProbabilidadesRequiem = [0.15,0.4,0.3,0.1,0.05]

s = 'Velocidad_Vida_Fuerza_Rango_Precision_Activacion'
formato = s.split('_')
with open('Ability.json','r') as f:
    file = json.load(f)

async def EstadisticasRequiem():
    ability = rd.choice(file)
    values = rd.choices(population = ValoresRequiem,weights = ProbabilidadesRequiem,k = 6)
    velocidad = rd.randint(47,53)
    PorncentajeVel = round((velocidad + (velocidad * (values[0] / 10))))
    HP = rd.randint(450,550)
    PorncentajeHP = round((HP + (HP * ((sum(values)/6) / 10))))
    Poder = rd.randint(100,105)
    PorncentajePoder = round((Poder + (Poder * (values[1] / 10))))
    Rango = rd.randint(10,20)
    PorncentajeRango = round((Rango + (Rango * (values[5] / 10))))
    Precision = 70 + (values[3] * 5)
    if ability['limitation']:
        if ability['type'] == 'self':
            if values[2] <= 0:
                values[2] = 0.3
            ability['value'][0] = (ability['value'][0] * values[2])
        else:
            ability['status'][1] += values[2]
    else:
        if values[2] <= 0:
            values[2] = 0.3
        for x in range(len(ability['value'])):
            ability['value'][x] = (ability['value'][x] * values[2])
    stats = {'Velocidad':PorncentajeVel,'Vida':PorncentajeHP,'Fuerza':PorncentajePoder,
    'Rango':PorncentajeRango,'Precision':Precision,'Activacion':6 - values[4],'Habilidad': ability}
    return values,stats

async def Estadisticas():
    ability = rd.choice(file)
    values = rd.choices(population = Valores,weights = Probabilidades,k = 6)
    velocidad = rd.randint(45,50)
    PorncentajeVel = round((velocidad + (velocidad * (values[0] / 10))))
    HP = rd.randint(400,500)
    PorncentajeHP = round((HP + (HP * ((sum(values)/6) / 10))))
    Poder = rd.randint(90,100)
    PorncentajePoder = round((Poder + (Poder * (values[1] / 10))))
    Rango = rd.randint(10,15)
    PorncentajeRango = round((Rango + (Rango * (values[5] / 10))))
    Precision = 65 + (values[3] * 5)
    if ability['limitation']:
        if ability['type'] == 'self':
            ability['value'][0] += (ability['value'][0] * values[2])
        else:
            ability['status'][1] += values[2]
    else:
        for x in range(len(ability['value'])):
            ability['value'][x] += (ability['value'][x] * values[2])
    stats = {'Velocidad':PorncentajeVel,'Vida':PorncentajeHP,'Fuerza':PorncentajePoder,
    'Rango':PorncentajeRango,'Precision':Precision,'Activacion':6 - values[4],'Habilidad': ability}
    return values,stats

async def Atributos(atributos):
    cadena = f'**Veloc {valor[atributos[0]]}\nPoder {valor[atributos[1]]}\nPoten {valor[atributos[2]]}\nPreci {valor[atributos[3]]}\nActiv {valor[atributos[4]]}\nRango {valor[atributos[5]]}**'
    return cadena

async def StringStats(stats):
    Estadistica = f'**❤ - Vida - {stats[formato[1]]}\n🔪 - Fuerza - {stats[formato[2]]}\n🏹 - Rango - {stats[formato[3]]} m\n🎯 - Precision - {stats[formato[4]]}%\n⚡ - Velocidad - {stats[formato[0]]}\n⏱ - Activacion - {stats[formato[5]]} Turno/s**'
    return Estadistica

async def Damage(atacante,victima,nombre):
    tiro = rd.randint(0,100)
    cadena = 'Nothing'
    victoria = False
    fuerza = atacante['Fuerza']
    if tiro <= atacante['Precision']:
        if atacante['Rango'] <= victima['position']:
            fuerza = round(fuerza - (fuerza * 0.2))
        if 'defend' in victima['status']:
            fuerza = round(fuerza - (fuerza * 0.4))
            victima['Vida'] -= fuerza
            victima['status'].remove('defend')
        else:
            victima['Vida'] -= fuerza
        knock = rd.randint(0,2)
        atacante['position'] += knock
        cadena = f'**{nombre}** ¡Acertaste tu ataque! Le quitaste **{fuerza}** ❤ de vida y lo alejaste **{knock} m**'
        if victima['Vida'] <= 0:
            cadena += f'\n!**{nombre}** a Ganado!'
            victoria = True         
    else:
        cadena = f'**{nombre}** Tu ataque a fallado'
    return victoria,cadena
    
async def ActivateAbility(stats,nombre):
    ability = stats['Habilidad']
    stats['Habilidad']['amount'] -= 1
    cadena = f'**{nombre}** has usado **『{ability["name"]}』**\n'
    if ability['limitation']:
        stat = stats[ability['stat'][0]]
        limitation = stats[ability['stat'][1]]
        values = ability['value']
        increase = round(stat + (stat * (values[0] / 10)))
        decrease = round(limitation - (limitation * (values[1] / 10)))
        stats[ability['stat'][0]] = increase
        stats[ability['stat'][1]] = decrease
        cadena += f'Tu **{ability["stat"][0]}** aumento a: **{str(increase)}**\nTu **{ability["stat"][1]}** se redujo a: **{str(decrease)}**'
    else:
        for x in range(len(ability['value'])):
            stat = stats[ability['stat'][x]]
            value = ability['value'][x]
            increase = round(stat + (stat * (value/ 10)))
            stats[ability['stat'][x]] = increase    
            cadena += f'Tu **{ability["stat"][x]}** aumento a: **{str(increase)}** \n'
    return cadena

async def TargetAbility(stats,enemigo,nombre,nombreEnemigo):
    ability = stats['Habilidad']
    ability['amount'] -= 1
    cadena = f'**{nombre}** has usado **『{ability["name"]}』** en **{nombreEnemigo}**\n'
    for x in range(len(ability['value'])):
        stat = enemigo[ability['stat'][x]]
        value = ability['value'][x]
        decrease = round(stat - (stat * (value/ 10)))
        enemigo[ability['stat'][x]] = decrease    
        cadena += f'La **{ability["stat"][x]}** de **{nombreEnemigo}** se redujo a: **{str(decrease)}**\n'
    if ability['limitation']:
        for x in ability['status']:
            enemigo['status'].append(x)
        cadena += f'**{nombre}** has aplicado el efecto de **{ability["status"][0]}** a **{nombreEnemigo}**'
    return cadena

async def Effect(stats,nombre):
    cadena = ''
    stop = False
    if 'Burn' in stats['status']:
        stats['Vida'] -= 40
        if stats['Vida'] > 0:
            cadena = f'\n{nombre} Pierdes **40 ❤** por las quemaduras'
        else:
            cadena = f'\n{nombre} Has perdido'
            stop = 'Die'
    elif 'Poison' in stats['status']:
        porcentaje = round(stats['Vida'] * 0.15)
        stats['Vida'] = stats['Vida'] - porcentaje
        cadena = f'\n{nombre} Pierdes **{porcentaje} ❤** por el veneno'
    elif 'Time Stop' in stats['status']:
        stop = True
        index = stats['status'].index('Time Stop') + 1
        stats['status'][index] -= 1
        cadena = f'\n{nombre} Estas detenido por {stats["status"][index]} Turno/s mas'
        if stats['status'][index] <= 0:
            stop = False
            stats['status'].remove('Time Stop')
            stats['status'].remove(0)
    return stop,cadena
    
