import discord
from discord.ext import commands
import asyncio
import random as rd
import Info,url,Stats

Objetos =  {0:"Flint",
            1:"Stick",
            2:"Feather",
            3:"Golden Flint",
            4:"Diamond Stick",
            5:"Golden Feather"}

inventory={'Flint':0,
            'Stick':1,
            'Feather':2,
            'Golden Flint':3,
            'Diamond Stick':4,
            'Golden Feather':5,
            'Arrow Stand':6,
            'Arrow Stand Requiem':7}

emojis = ['<:Flint:811814638639251457>','<:Stick:811814638983315497>',
'<:Feather:811814638630993920>','<:GoldenFlint:811840577901035543>',
'<:DiamondStick:811840519352221706>','<:GoldenFeather:811840519113015297>',
'<:StandArrow:811814640744529922>','<:StandArrow:811814640744529922>']

valor = [-1,0,1,2,3,4,5]
Probabilidades = [0.2,0.24,0.24,0.27,0.01,0.01,0.03]
#cantidades = [1,2,3]
#ProbabilidadesC = [0.8,0.15,0.5]

class Items(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    async def CheckExiste(ctx):
        return await Info.Existe(ctx.author)

    @commands.command()
    async def Start(self,ctx):
        Inicio = await Info.Existe(ctx.author)
        if not Inicio:
            await ctx.send('Te ves fuerte, Espero no me decepciones')
            await ctx.send('https://i.imgur.com/ee3wzUd.gif')
            stand = await url.nombre()
            values,stats = await Stats.Estadisticas()
            Inicio = await Info.GuardarUsuario(ctx.author,values,stand,stats)
            await ctx.send('¡Ahora tienes un Stand!')
        else:
            await ctx.send('A ti ya te di una flecha asi que no me decepciones')
        
    @commands.command()
    @commands.check(CheckExiste)
    @commands.cooldown(rate = 1,per = 5, type = commands.BucketType.user)
    async def Use(self,ctx,*,objeto:str = None):
        if not objeto:
            await ctx.send('Debes poner el nombre del objeto que deseas usar')
        else:
            objeto = objeto.lower()
            inventario = await Info.GetObjetos(ctx.author)
            if objeto in ('arrow stand','as'):
                await Usar(inventario,'Arrow Stand',ctx)
            elif objeto in ('arrow stand requiem','asr'):
                await Usar(inventario,'Arrow Stand Requiem',ctx)
            else:
                await ctx.send(f'Este no es un objeto valido')

    @commands.command()
    @commands.check(CheckExiste)
    @commands.cooldown(rate = 1,per = 15, type = commands.BucketType.user)
    async def Explore(self,ctx):
        objeto = rd.choices(population = valor,weights = Probabilidades)
        if objeto[0] != -1:
            #cantidad = rd.choices(population = cantidades,weights = ProbabilidadesC)
            await Info.GuardarObjeto(ctx.author,Objetos[objeto[0]],1)
            await ctx.send(f'Exploraste un poco y Encontraste: **1 {Objetos[objeto[0]]}** {emojis[objeto[0]]}')
        else:
            await ctx.send('Lo intentaste pero no encontraste nada')

    @commands.command()
    @commands.check(CheckExiste)
    async def Inventory(self,ctx):
        inventario = await Info.GetObjetos(ctx.author)
        embedVar = discord.Embed(title = '**__Inventario__**', color = discord.Color.red())
        materiales = '-'
        consumibles = '-'
        for key, value in inventario.items():
            if value > 0:
                if inventory[key] <= 5:
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
        embedVar.add_field(name = '**『 Arrow Stand 』**', value = '**<:Flint:811814638639251457> + <:Stick:811814638983315497> + <:Feather:811814638630993920> = <:StandArrow:811814640744529922>**',inline = False) 
        embedVar.add_field(name = '**『 Arrow Stand Requiem』**',value =' **<:GoldenFlint:811840577901035543> + <:DiamondStick:811840519352221706> + <:GoldenFeather:811840519113015297> = ** *Emoji de la flecha requiem xd*',inline = False )
        await ctx.send(embed = embedVar)
        

    @commands.command()
    @commands.check(CheckExiste)
    async def Craft(self,ctx,*,objeto:str = None):
        if not objeto:
            await ctx.send('Debes poner el nombre del objeto que deseas crear')
        else:
            objeto = objeto.lower()
            inventario = await Info.GetObjetos(ctx.author)
            if objeto in ('arrow stand','as'):
                    await Craftear(inventario,'Flint','Stick','Feather','Arrow Stand',ctx)
            elif objeto in ('arrow stand requiem','asr'):
                    await Craftear(inventario,'Golden Flint','Diamond Stick','Golden Feather','Arrow Stand Requiem',ctx)
            else:
                await ctx.send(f'Este no es un objeto valido')

async def Usar(inventario,objeto,ctx):
    if inventario[objeto] > 0:
        stand = await url.nombre()
        values,stats = await Stats.Estadisticas()
        await Info.GuardarStand(user = ctx.author, atributos = values, stand = stand, stats = stats,objeto = objeto)
        await ctx.send('https://media1.tenor.com/images/36d30efef07ecae295d330588618fc8b/tenor.gif?itemid=14490536')
    else:
        await ctx.send('No tienes mas de este objeto')

async def Craftear(inventario,objeto1,objeto2,objeto3,creacion,ctx):
    if inventario[objeto1] > 0 and inventario[objeto2] > 0 and inventario[objeto3] > 1 :
        inventario[objeto1] -= 1
        inventario[objeto2] -= 1
        inventario[objeto3] -= 2
        inventario[creacion] += 1
        await Info.GuardarInventario(ctx.author,inventario)
        await ctx.send(f'El objeto ***{creacion}*** a sido creado')
    else:
        await ctx.send(f'No tienes suficientes materiales para crear ***{creacion}***')

def setup(bot):
    bot.add_cog(Items(bot))