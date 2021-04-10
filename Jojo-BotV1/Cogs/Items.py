import discord
from discord.ext import commands
import asyncio
import random as rd
import Info,url,Stats
import json

Objetos =  {0:"Flint",
            1:"Stick",
            2:"Feather",
            3:"Golden Flint",
            4:"Diamond Stick",
            5:"Golden Feather",
            6:"Meteorite"}

inventory={'Flint':0,
            'Stick':1,
            'Feather':2,
            'Golden Flint':3,
            'Diamond Stick':4,
            'Golden Feather':5,
            'Meteorite':6,
            'Stand Arrow':7,
            'Stand Arrow Requiem':8,
            'Ability Arrow':9,
            'Stone Pendant':10,
            'Stone Mask':11,
            'Red Stone Of Aja':12,
            'Stone Mask With The Red Stone':13
            }

emojis = ['<:Flint:811814638639251457>','<:Stick:811814638983315497>','<:Feather:811814638630993920>',
'<:GoldenFlint:811840577901035543>','<:DiamondStick:811840519352221706>','<:GoldenFeather:811840519113015297>',
'<:StandMeteorite:817954014481350698>','<:StandArrow:811814640744529922>','<:StandArrowRequiem:814300958484856864>',
'<:AbilityArrow:818650694033866752>','<:StonePendant:818653936448831563>',
'<:StoneMask:814297491021103115>','<:RedStoneOfAja:814298072473272322>','<:StoneMaskWithTheRedStone:814311812068802601>']

with open('Ability.json','r') as f:
    file = json.load(f)

valor = [-1,0,1,2,3,4,5,6]
Probabilidades = [0.13,0.16,0.16,0.16,0.03,0.03,0.03,0.3]
cantidades = [1,2,3]
ProbabilidadesC = [0.89,0.1,0.01]

class Items(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    async def CheckExiste(ctx):
        return await Info.Existe(ctx.author)

    @commands.command(aliases=['IO'])
    async def InfoObjects(self,ctx):
        embedVar = discord.Embed(title = "Informacion Objetos", color = discord.Colour.random())
        embedVar.add_field(name = 'Materiales',value = '❌ Nada: **13%**\n<:Flint:811814638639251457> Flint: **16%**\n<:Stick:811814638983315497> Stick: **16%**\n<:Feather:811814638630993920> Feather: **16%**\n<:GoldenFlint:811840577901035543> Golden Flint: **3%**\n<:DiamondStick:811840519352221706> Diamond Stick: **3%**\n<:GoldenFeather:811840519113015297> Golden Feather: **3%**\n<:StandMeteorite:817954014481350698> Meteorite: **30%**')
        embedVar.add_field(name = 'Objetos',value = '<:StandArrow:811814640744529922> **Stand Arrow:** Invocas un nuevo stand\n- 0: **20%**  - 1: **40%**  - 2: **25%**  - 3: **10%**  - 4: **4.5%**  - 5: **0.5%** -\n<:StandArrowRequiem:814300958484856864> **Stand Arrow Requiem:** Invocas un nuevo stand mas poderoso\n- 1: ** 15%**  - 2: ** 40%**  - 3: ** 30%**  - 4: ** 10%**  - 5: ** 5%** -\n<:AbilityArrow:818650694033866752> **Ability Arrow:** Cambias tu habilidad con otra al azar\n<:StonePendant:818653936448831563> **Stone Pendant:** Aumentas en **1 nivel** tu atributo mas bajo',inline = False)
        await ctx.send(embed = embedVar)

    @commands.command()
    async def Start(self,ctx):
        Inicio = await Info.Existe(ctx.author)
        if not Inicio:
            EmbedVar = discord.Embed()
            EmbedVar.add_field(name = 'Te ves fuerte, Espero no me decepciones', value = '¡Ahora tienes un Stand!')
            EmbedVar.set_image(url = 'https://i.imgur.com/ee3wzUd.gif')
            EmbedVar.set_footer(text = f'Para ver tu stand utiliza el comando {ctx.prefix}Stand')
            stand = await url.nombre()
            values,stats = await Stats.Estadisticas()
            Inicio = await Info.GuardarUsuario(ctx.author,values,stand,stats)
            await ctx.send(embed = EmbedVar)
        else:
            await ctx.send('A ti ya te di una flecha asi que no me decepciones')
        
    @commands.command()
    @commands.check(CheckExiste)
    #@commands.cooldown(rate = 2,per = 5, type = commands.BucketType.user)
    async def Use(self,ctx,*,objeto:str = None):
        if not objeto:
            await ctx.send('Debes poner el nombre del objeto que deseas usar')
        else:
            objeto = objeto.lower()
            inventario = await Info.GetObjetos(ctx.author)
            if objeto in ('stand arrow','sa'):
                await Usar(inventario,'Stand Arrow',ctx)
            elif objeto in ('stand arrow requiem','sar'):
                await Usar(inventario,'Stand Arrow Requiem',ctx)
            elif objeto in ('ability arrow','aa'):
                await Usar(inventario,'Ability Arrow',ctx)
            elif objeto in ('stone pendant','sp'):
                await Usar(inventario,'Stone Pendant',ctx)
            else:
                await ctx.send('Este no es un objeto valido')

    @commands.command(aliases=['EX'])
    @commands.check(CheckExiste)
    #@commands.cooldown(rate = 1,per = 15, type = commands.BucketType.user)
    async def Explore(self,ctx):
        objeto = rd.choices(population = valor,weights = Probabilidades)
        if objeto[0] != -1:
            cantidad = rd.choices(population = cantidades,weights = ProbabilidadesC)
            await Info.GuardarObjeto(ctx.author,Objetos[objeto[0]],cantidad[0])
            await ctx.send(f'Exploraste un poco y Encontraste: **{cantidad[0]} {Objetos[objeto[0]]}** {emojis[objeto[0]]}')
        else:
            await ctx.send('Lo intentaste pero no encontraste nada')

    @commands.command(aliases=['SPW'])
    @commands.check(CheckExiste)
    async def SpeedWagonFoundation(self,ctx):
        embedVar = discord.Embed(title = '**__SpeedWagon Foundation__**', color = discord.Color.blurple())
        embedVar.add_field(name = '<:StoneMask:814297491021103115> Stone Mask',value = '***3000*** Puntos de Reputacion', inline = False)
        embedVar.add_field(name = '<:RedStoneOfAja:814298072473272322> Red Stone of Aja',value = '***5000*** Puntos de Reputacion')
        await ctx.send(embed = embedVar)

    @commands.command(aliases=['i','inv'])
    @commands.check(CheckExiste)
    async def Inventory(self,ctx):
        inventario = await Info.GetObjetos(ctx.author)
        embedVar = discord.Embed(title = '**__Inventario__**', color = discord.Color.red())
        embedVar.set_footer(text = f'Si necesitas informacion de algun objeto usar el comando {ctx.prefix}InfoObjects')
        materiales = '-'
        consumibles = '-'
        for key, value in inventario.items():
            if value > 0:
                if inventory[key] <= 6:
                    materiales += f'{emojis[inventory[key]]} **{key} : {value}** \n'
                else:
                    consumibles += f'{emojis[inventory[key]]} **{key} : {value}** \n'
        embedVar.add_field(name = '**__Materiales__**',value = materiales, inline = False)
        embedVar.add_field(name = '**__Consumibles__**',value = consumibles)
        await ctx.send(embed = embedVar)

    @commands.command()
    @commands.check(CheckExiste)
    async def Recipes(self,ctx):
        color = discord.Colour.random()
        embedVar = discord.Embed(title = "Recetas", color = color)
        embedVar.add_field(name = '**『 Stand Arrow 』**', value = '**<:StandMeteorite:817954014481350698> + <:StandMeteorite:817954014481350698> + <:Flint:811814638639251457> + <:Stick:811814638983315497> + <:Feather:811814638630993920> = <:StandArrow:811814640744529922>**',inline = False) 
        embedVar.add_field(name = '**『 Stand Arrow Requiem 』**',value =' **<:StandMeteorite:817954014481350698> + <:StandMeteorite:817954014481350698> + <:GoldenFlint:811840577901035543> + <:DiamondStick:811840519352221706> + <:GoldenFeather:811840519113015297> = ** <:StandArrowRequiem:814300958484856864> ',inline = False )
        embedVar.add_field(name = '**『 Ability Arrow 』**', value = '**<:StandMeteorite:817954014481350698> + <:Stick:811814638983315497> + <:Feather:811814638630993920> = <:AbilityArrow:818650694033866752>**',inline = False) 
        embedVar.add_field(name = '**『 Stone Pendant 』**', value = '**<:StandMeteorite:817954014481350698> + <:Flint:811814638639251457> + <:GoldenFlint:811840577901035543> = <:StonePendant:818653936448831563>**',inline = False)
        embedVar.add_field(name = '**『 Stone Mask with the Red Stone 』**',value =' **<:StoneMask:814297491021103115> + <:RedStoneOfAja:814298072473272322> = ** <:StoneMaskWithTheRedStone:814311812068802601>',inline = False )
        await ctx.send(embed = embedVar)

    @commands.command()
    @commands.check(CheckExiste)
    async def Craft(self,ctx,*,objeto:str = None):
        if not objeto:
            await ctx.send('Debes poner el nombre del objeto que deseas crear')
        else:
            objeto = objeto.lower()
            inventario = await Info.GetObjetos(ctx.author)
            if objeto in ('stand arrow','sa'):
                    await Craftear(inventario,'Flint','Stick','Feather','Meteorite','Stand Arrow',ctx)
            elif objeto in ('stand arrow requiem','sar'):
                    await Craftear(inventario,'Golden Flint','Diamond Stick','Golden Feather','Meteorite','Stand Arrow Requiem',ctx)
            elif objeto in ('ability arrow','aa'):
                    await Craftear2(inventario,['Meteorite','Flint','Feather'],'Ability Arrow',ctx)
            elif objeto in ('stone pendant','sp'):
                    await Craftear2(inventario,['Meteorite','Stick','Golden Flint'],'Stone Pendant',ctx)
            else:
                await ctx.send(f'Este no es un objeto valido')


async def Usar(inventario,objeto,ctx):
    if inventario[objeto] > 0:
        if objeto == 'Stand Arrow':
            stand = await url.nombre()
            values,stats = await Stats.Estadisticas()
            await Info.GuardarStand(user = ctx.author, atributos = values, stand = stand, stats = stats,objeto = objeto)
            await ctx.send('https://media1.tenor.com/images/36d30efef07ecae295d330588618fc8b/tenor.gif?itemid=14490536')
        elif objeto == 'Stand Arrow Requiem':
            stand = await url.nombre()
            values,stats = await Stats.EstadisticasRequiem()
            await Info.GuardarStand(user = ctx.author, atributos = values, stand = stand, stats = stats,objeto = objeto)
            await ctx.send('https://i.imgur.com/nt4GeCq.gif')
        elif objeto == 'Ability Arrow':
            stand,atributos,stats = await Info.GetInfo(ctx.author)
            ability = rd.choice(Stats.file)
            while stats['Habilidad']['name'] == ability['name']:
                ability = rd.choice(Stats.file)
            if ability['limitation']:
                if ability['type'] == 'self':
                    ability['value'][0] = (ability['value'][0] * atributos[2])
                else:
                    ability['status'][1] += atributos[2]
            else:
                for x in range(len(ability['value'])):
                    ability['value'][x] = (ability['value'][x] * atributos[2])
            stats['Habilidad'] = ability
            await Info.GuardarStand(user = ctx.author, atributos = atributos, stand = stand, stats = stats,objeto = objeto)
            await ctx.send('¡Cambiaste tu habilidad exitosamente! <a:Naisss:808550986711826503>')
        elif objeto == 'Stone Pendant':
            cadena = ''
            stand,atributos,stats = await Info.GetInfo(ctx.author)
            minimo = min(atributos)
            index = atributos.index(minimo)
            if minimo < 4:
                atributos[index] += 1
                if index == 0:
                    cadena = 'Velocidad'
                    velocidad = stats['Velocidad']
                    stats['Velocidad'] = round((velocidad + (velocidad * 0.3)))
                elif index == 1:
                    cadena = 'Poder'
                    Poder = stats['Fuerza']
                    stats['Fuerza'] = round((Poder + (Poder * 0.2)))
                elif index == 2:
                    cadena = 'Potencia'
                    archivos = file
                    ability = stats['Habilidad']
                    for archivo in archivos:
                        if archivo['name'] == stats['Habilidad']['name']:
                            if ability['limitation']:
                                if ability['type'] == 'self':
                                    ability['value'][0] = (archivo['value'][0] * atributos[2])
                                else:
                                    ability['status'][1] += 1
                            else:
                                for x in range(len(archivo['value'])):
                                    ability['value'][x] = (archivo['value'][x] * atributos[2])
                            stats['Habilidad'] = ability
                            break
                elif index == 3:
                    cadena = 'Precision'
                    Precision = stats['Precision']
                    stats['Precision'] = Precision + 5
                elif index == 4:
                    cadena = 'Activacion'
                    stats['Activacion'] = 6 - atributos[4]
                elif index == 5:
                    cadena = 'Rango'
                    Rango = stats['Rango']
                    stats['Rango'] = round((Rango + (Rango * 0.2)))
                await Info.GuardarStand(user = ctx.author, atributos = atributos, stand = stand, stats = stats,objeto = objeto)
                await ctx.send(f'¡Tu **{cadena}** aumento 1 nivel! <a:Naisss:808550986711826503>')
            else:
                await ctx.send(f'¡Ya tienes todos tus atributos al maximo!')
    else:
        await ctx.send('No tienes este objeto')

async def Craftear(inventario,objeto1,objeto2,objeto3,objeto4,creacion,ctx):
    if inventario[objeto1] > 0 and inventario[objeto2] > 0 and inventario[objeto3] > 0 and inventario[objeto4] > 1:
        inventario[objeto1] -= 1
        inventario[objeto2] -= 1
        inventario[objeto3] -= 1
        inventario[objeto4] -= 2
        inventario[creacion] += 1
        await Info.GuardarInventario(ctx.author,inventario)
        await ctx.send(f'El objeto ***{creacion}*** a sido creado')
    else:
        await ctx.send(f'No tienes suficientes materiales para crear ***{creacion}***')

async def Craftear2(inventario,objetos,creacion,ctx):
    if inventario[objetos[0]] > 0 and inventario[objetos[1]] > 0 and inventario[objetos[2]] > 0:
        for x in range(len(objetos)):
            inventario[objetos[x]] -= 1
        inventario[creacion] += 1
        await Info.GuardarInventario(ctx.author,inventario)
        await ctx.send(f'El objeto ***{creacion}*** a sido creado')
    else:
        await ctx.send(f'No tienes suficientes materiales para crear ***{creacion}***')

def setup(bot):
    bot.add_cog(Items(bot))