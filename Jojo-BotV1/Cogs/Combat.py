import discord
from discord.ext import commands
import asyncio
import random as rd
import Info, url, Stats,test
from io import BytesIO


punto = {0: 'Con todo el cuerpo', 1: 'Con las Manos', 2: 'Pulsando un botón',
         3: 'A voluntad del usuario', 4: 'Con Un arma', 5: 'Abriendo algo',
         6: 'Frotando tu talón', 7: 'Con las Rodillas', 8: 'Cerrando los ojos',
         9: 'Mordiendo', 10: 'Con las Muñecas', 11: 'Con un chasquido',
         12: 'Hablando', 13: 'Con las piernas', 14: 'Con ganas de morir',
         15: 'Con miedo', 16: 'Usando algun objeto', 17: 'Con dolor'}

demomento = ['Eder','El pepe','El onichan','Un michi','L U I S','<a:MORITE:806684100249124864>',
'Dio','Drim','Hayase','Chino','Giorno','Lapis','Bodoque','<:Planmalo:799402450431115287>',
'El esteban Re fan de jojos']

valor = [0,1,2,3,4,5,6]
Probabilidades = [0.18,0.18,0.18,0.02,0.02,0.02,0.4]

Objetos =  {0:"Flint",
            1:"Stick",
            2:"Feather",
            3:"Golden Flint",
            4:"Diamond Stick",
            5:"Golden Feather",
            6:"Meteorite"}

emojis = ['<:Flint:811814638639251457>','<:Stick:811814638983315497>',
'<:Feather:811814638630993920>','<:GoldenFlint:811840577901035543>',
'<:DiamondStick:811840519352221706>','<:GoldenFeather:811840519113015297>','<:StandMeteorite:817954014481350698>']

class Combat(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases=['IS'])
    async def InfoStands(self,ctx):
        embedVar = discord.Embed(title = "Informacion Stands", description = 'Una pequeña intoduccion a la mecanica de los Stands', color = discord.Colour.random())
        embedVar.add_field(name = 'Stands',
        value = '**__Atributos__**\n**- Velocidad:** Velocidad stand\n**- Poder:** Fuerza stand\n**- Potencia:** Potencia de las habilidades\n**- Precision:** Precision stand\n**- Activacion:** Cantidad de turnos reducidos para activar habilidad\n**- Rango:** Rango maximo stand\n**__Valores:__**\n Los valores de los atributos van desde 0 hasta 5 y aumentan sus respectivas estadisticas\n0 : 0%\n1 : 10%\n2 : 20%\n3 : 30%\n4 : 40%\n5 : 50%\n**__Estadisticas:__**\n- **Velocidad**: El stand que tenga la mayor velocidad atacara primero en cada turno\n- **Vida**: La vida del stand\n- **Fuerza**: La Fuerza del stand\n- **Rango**: La distancia maxima de alcanze del stand, si el stand no tiene suficiente rango para alcanzar el stand enemigo su daño se reduce un 30%\n- **Precision**: La precision de los ataque del stand, entre mas alto mas probable de acertar el ataque\n- **Activacion**: La cantidad de turnos necesarios para utilizar la habilidad de tu stand')
        await ctx.send(embed = embedVar)

    @commands.command()
    async def Top(self,ctx):
        XD = await Info.GetReputaciones()
        XDDD = ''
        P = 1
        primero = self.bot.get_user(XD[0]["_id"])
        Cosa = discord.Embed(title = "Top", description = 'El top de reputacion de jugadores', color = discord.Color.dark_blue())
        Cosa.set_thumbnail(url = primero.avatar_url)
        for x in XD:
            XDDD += f'**{P}- {self.bot.get_user(x["_id"])}** reputacion: **{x["reputacion"]}**\n'
            P += 1
        Cosa.add_field(name = 'Jugadores', value = XDDD)
        await ctx.send(embed = Cosa)

    @commands.command()
    async def Stand(self,ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        datos = await Info.GetInfo(member)
        if not datos:
            await ctx.reply('Debes usar primero Start para obtener un stand y usar estos comandos')
        else:
            stand = datos[0]
            values = datos[1]
            stats = datos[2]
            atributos = await Stats.Atributos(values)
            Estadisticas = await Stats.StringStats(stats = stats)
            color = discord.Colour.random()
            embedVar = discord.Embed(title = "Stand", description = f'**『 {stand} 』**', color = color)
            embedVar.add_field(name ="Nombre Stand Master", value = member.mention, inline=False)
            embedVar.add_field(name ="Estadisticas", value = Estadisticas, inline=False)
            embedVar.add_field(name ="Atributos", value = atributos, inline=False)
            embedVar.add_field(name ="Habilidad", value = f"**『 {stats['Habilidad']['name']}』**", inline=False)
            embedVar.set_thumbnail(url = member.avatar_url)
            embedVar.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
            embedVar.set_footer(text = f'Para tener mas informacion sobre los datos pon {ctx.prefix}InfoStands')
            await ctx.send(embed = embedVar)

    @commands.command()
    @commands.cooldown(rate = 1,per = 2.5, type = commands.BucketType.channel)
    @commands.max_concurrency(number = 3, per = commands.BucketType.guild)
    async def Stats(self,ctx, *, member: discord.Member = None):
        async with ctx.channel.typing():
            if not member:
                member = ctx.message.author
            nombre = member.name
            datos = await Info.GetInfo(member)
            if not datos:
                await ctx.reply('Debes usar primero Start para obtener un stand y usar estos comandos')
            else:
                stand = datos[0]
                values = datos[1]
                asset = member.avatar_url_as(size=256)
                pfp = BytesIO(await asset.read())
                Imagen = await test.Fondo(nombre= nombre,nick= stand,data=pfp,values = values)
                arr = BytesIO()
                Imagen.save(arr, format='JPEG')
                arr.seek(0)
                await ctx.send(file = discord.File(arr, 'Stats.png'))
                arr.close()


    @commands.command(aliases=['A'])
    async def Ability(self,ctx):
        datos = await Info.GetInfo(ctx.author)
        if not datos:
            await ctx.reply('Debes usar primero Start para obtener un stand y usar estos comandos')
        else:
            color = discord.Colour.random()
            #info = await url.get_info()
            stand = datos[0]
            stats = datos[2]
            cadena = ''
            habilidad = stats['Habilidad']
            embedVar = discord.Embed(timestamp = ctx.message.created_at,color = color)
            embedVar.set_author(name = ctx.author,icon_url=ctx.author.avatar_url)
            embedVar.add_field(name='Nombre Stand',value= f'『**{stand}**』') 
            embedVar.add_field(name='Nombre Habilidad',value = f"『**{habilidad['name']}**』")
            embedVar.add_field(name='Nivel Habilidad',value= f"{datos[1][2]}")
            embedVar.add_field(name='Descripcion',value = habilidad['description'], inline=False)
            embedVar.add_field(name='Metodo de activacion',value=rd.choice(punto))
            embedVar.add_field(name='Cantidad de usos',value= f"{habilidad['amount']}")
            for value in habilidad["value"]:
                cadena += f'{round(value * 10)}% '
            embedVar.add_field(name='Porcentajes',value= cadena)
            embedVar.add_field(name='Tipo de habilidad',value= f"{habilidad['type']}")
            
            await ctx.send(embed=embedVar)

    @commands.command()
    @commands.cooldown(rate = 1,per = 60, type = commands.BucketType.member)
    async def Combat(self,ctx):
        nombreRetador = ctx.author.name
        retador = await Info.GetInfo(ctx.author)
        if not retador:
            await ctx.send(f'{ctx.author.mention} Aun no has despertado tu stand, para hacerlo usa el comando Start')
            self.bot.get_command("Combat").reset_cooldown(ctx)
        elif await Info.GetEnBatalla(ctx.author):
            await Info.EnBatallaC([ctx.author],True)
            #stand = await url.nombre()
            NombreBot = rd.choice(demomento)
            values,Enemigo = await Stats.Estadisticas()
            stand = Enemigo['Habilidad']['name']
            await ctx.send(f'{ctx.author.mention} ¡{NombreBot} Te a retado a un duelo!')
            #retadorStats = await Stats.StringStats(retador[2])
            #enemigoStats = await Stats.StringStats(Enemigo)
            retador[2]['status'] = []
            Enemigo['status'] = []
            retador[2]['position'] = retador[2]['Rango']
            Enemigo['position'] = Enemigo['Rango']
            '''Inicio = discord.Embed(title = "Challenge", description = f'**{nombreRetador}** VS **{NombreBot}**',colour = discord.Colour.blurple())
            Inicio.add_field(name =  f'**『 {retador[0]} 』**', value = retadorStats)
            Inicio.add_field(name =  f'**『 {stand} 』**', value = enemigoStats)
            await ctx.send(embed = Inicio)'''
            await CombateBot(ctx.author,NombreBot,retador[2],Enemigo,ctx,self.bot)
            if retador[2]['Vida'] <= 0:
                await ctx.send(f'{ctx.author.mention} No conseguiste nada de esta batalla')
            else:
                objeto = rd.choices(population = valor,weights = Probabilidades)
                await Info.GuardarObjeto(ctx.author,Objetos[objeto[0]],1)
                await ctx.send(f'Coneguiste: **1 {Objetos[objeto[0]]}** {emojis[objeto[0]]} Por ganar esta batalla \nGanaste **10** de reputacion')
            await Info.EnBatallaC([ctx.author],False)
            await Info.SetReputacion(ctx.author,10)
        else:
            self.bot.get_command("Combat").reset_cooldown(ctx)
            await ctx.send('Estas en una batalla ahora mismo')
        
    @commands.command()
    @commands.cooldown(rate = 1,per = 60, type = commands.BucketType.member)
    async def Challenge(self,ctx, *, member: discord.Member = None):
        if not member or member is ctx.author:
            self.bot.get_command("Challenge").reset_cooldown(ctx)
            await ctx.send('Debes mencionar a alguien para retarlo')
        else:
            nombreRetador = ctx.author.name
            nombreDesafiado = member.name
            retador = await Info.GetInfo(ctx.author)
            desafiado = await Info.GetInfo(member)
            if not retador or not desafiado:
                self.bot.get_command("Challenge").reset_cooldown(ctx)
                await ctx.send('Uno de los dos usuarios no a despertado su stand, para hacerlo utiliza Start')
            elif await Info.GetEnBatalla(ctx.author) and await Info.GetEnBatalla(member):
                await Info.EnBatallaC([ctx.author,member],True)
                await ctx.send(f'{member.mention} ¡Te han retado a un duelo! \n¿Aceptas? yes / no')
                def check(m):
                    return m.channel == ctx.channel and m.author == member and m.content.lower() in ('yes','y','no','n')
                try:
                    msg = await self.bot.wait_for('message', timeout = 30.0, check=check)
                except asyncio.TimeoutError:
                    await Info.EnBatallaC([ctx.author,member],False)
                    self.bot.get_command("Challenge").reset_cooldown(ctx)
                    await ctx.send('Te demoraste mucho <:JojoThinking:801507786109222932>')
                else:
                    if msg.content.lower() in ('no','n'):
                        self.bot.get_command("Challenge").reset_cooldown(ctx)
                        await Info.EnBatallaC([ctx.author,member],False)
                        await ctx.send('El duelo ha sido rechazado')
                    else:
                        '''retadorStats = await Stats.StringStats(retador[2])
                        desafiadoStats = await Stats.StringStats(desafiado[2])
                        Inicio = discord.Embed(title = "Challenge", description = f'**{nombreRetador}** VS **{nombreDesafiado}**',colour = discord.Colour.dark_theme())
                        Inicio.add_field(name =  f'**『 {retador[0]} 』**', value = retadorStats)
                        Inicio.add_field(name =  f'**『 {desafiado[0]} 』**', value = desafiadoStats)
                        await ctx.send(embed = Inicio)'''
                        retador[2]['status'] = []
                        desafiado[2]['status'] = []
                        retador[2]['position'] =  retador[2]['Rango']
                        desafiado[2]['position'] = desafiado[2]['Rango']
                        await Combate(ctx.author,member,retador[2],desafiado[2],ctx,self.bot)
                        await Info.EnBatallaC([ctx.author,member],False)
                        if retador[2]['Vida'] <= 0:
                            await Info.SetReputacion(member,100)
                            await ctx.send(f'{member} a ganado **100** puntos de reputacion')
                        else:
                            await Info.SetReputacion(ctx.author,100)
                            await ctx.send(f'{ctx.author} a ganado **100** puntos de reputacion')
            else:
                self.bot.get_command("Challenge").reset_cooldown(ctx)
                await ctx.send('Uno de los jugadores esta en una batalla ahora mismo')
                

async def Combate(nombreRetador,nombreDesafiado,retador,desafiado,ctx,bot):
    continuar = True
    Respuesta = discord.Embed(colour = discord.Colour.gold())
    Respuesta.add_field(name = 'Descion',value = 'Resultado')
    for turno in range(1,151):
        if retador['Velocidad'] >= desafiado['Velocidad']:
            continuar = await Turno(nombreRetador,nombreDesafiado,ctx,retador,desafiado,turno,bot,Respuesta)
            if continuar:
                continuar = await Turno(nombreDesafiado,nombreRetador,ctx,desafiado,retador,turno,bot,Respuesta)
        else:
            continuar = await Turno(nombreDesafiado,nombreRetador,ctx,desafiado,retador,turno,bot,Respuesta)
            if continuar:
                continuar = await Turno(nombreRetador,nombreDesafiado,ctx,retador,desafiado,turno,bot,Respuesta)
        if not continuar:
            break

async def Turno(atacante,siguienteAtacante,ctx,stat,statSiguiente,turno,bot,Respuesta):
    Respuesta.set_author(name = atacante,icon_url = atacante.avatar_url)
    stop,effect = await Stats.Effect(stat,atacante)
    if stop:
        Respuesta.set_field_at(0,name = 'Time Stop',value = effect)
        Respuesta.set_image(url = 'https://thumbs.gfycat.com/FrankAlarmingAyeaye-max-1mb.gif')
        await ctx.send(embed = Respuesta)
        Respuesta.set_image()
        return True
    elif stop == 'Die':
        Respuesta.set_field_at(0,name = 'Derrota',value = effect)
        await ctx.send(embed = Respuesta)
    cadena = ''
    retadorStats = await Stats.StringStats(stat)
    desafiadoStats = await Stats.StringStats(statSiguiente)
    Inicio = discord.Embed(title = f'Turno: **{turno}**',colour = discord.Colour.gold())
    Inicio.add_field(name =  f'**『 {atacante} 』**', value = retadorStats)
    Inicio.add_field(name =  f'**『 {siguienteAtacante} 』**', value = desafiadoStats)
    Inicio.add_field(name = f'Turno de **{atacante}**',value = f'Distancia hasta Enemigo: **{statSiguiente["position"]} m**{effect} \n\nDecide tu accion: \n\n**Attack - Ability - Defend - Approach - Nigerundayo**',inline = False)
    await ctx.send(embed = Inicio)
    def check(m):
        return m.channel == ctx.channel and m.author == atacante and  m.content.lower() in ('attack','ability','approach','nigerundayo','defend')
    try:
        msg = await bot.wait_for('message', timeout = 20.0, check=check)
    except asyncio.TimeoutError:
        stat['Vida'] -= 50
        if stat['Vida'] <= 0:
            Respuesta.set_field_at(0,name = 'Derrota',value = f'**{siguienteAtacante}** a ganado')
            await ctx.send(embed = Respuesta)
            return False
        Respuesta.set_field_at(0,name = 'Inactividad',value = f'**{atacante}** Te has demorado mucho para responder, pierdes **50 ❤**')
        await ctx.send(embed = Respuesta)
        return True
    else:
        eleccion = msg.content.lower()
        if eleccion == 'attack':
            victoria,cadena = await Stats.Damage(stat,statSiguiente,atacante)
            Respuesta.set_field_at(0,name = 'Ataque',value = cadena)
            await ctx.send(embed = Respuesta)
            return not victoria
        elif eleccion == 'ability':
            if stat['Habilidad']['amount'] > 0:
                if stat['Activacion'] <= turno:
                    if stat['Habilidad']['type'] == 'self':
                        cadena = await Stats.ActivateAbility(stat,atacante)
                    else:
                        cadena = await Stats.TargetAbility(stat,statSiguiente,atacante,siguienteAtacante)
                else:
                    cadena = f'**{atacante}** Aun no puedes activar tu habilidad, puedes activarla desde el turno **{stat["Activacion"]}**'
            else:
                cadena = f'**{atacante}** Ya usaste tu habilidad en esta batalla'
            Respuesta.set_field_at(0,name = 'Habilidad',value = cadena)
            await ctx.send(embed = Respuesta)
            return True
        elif eleccion == 'defend':
            if not 'defend' in stat['status']:
                cadena = f'**{atacante}** Te defiendes del proximo ataque enemigo'
                stat['status'].append('defend')
            else:
                cadena = f'**{atacante}** ¡Ya te estas defendiendo del proximo ataque!'
            Respuesta.set_field_at(0,name = 'Defensa',value = cadena)
            await ctx.send(embed = Respuesta)
            return True
        elif eleccion == 'approach':
            closer = rd.randint(5,10)
            Respuesta.set_field_at(0,name = 'Acercarse',value = f'**{atacante}** Te acercas **{closer} m** hacia el enemigo de manera ***Amenazadora*** y ganas **2%** de precision')
            await ctx.send(embed = Respuesta)
            stat['Precision'] += 2
            statSiguiente['position'] -= closer
            if statSiguiente['position'] < 0:
                statSiguiente['position'] = 0
            return True
        else:
            stat['Vida'] = 0
            Respuesta.set_field_at(0,name = 'Nigerundayo',value = f'Saliste corriendo de la batalla \n**{siguienteAtacante}** a ganado')
            Respuesta.set_image(url = 'https://media1.tenor.com/images/8dcdd7d0a9459951fddac8f0f116e299/tenor.gif?itemid=15566885')
            await ctx.send(embed = Respuesta)
            return False

async def CombateBot(nombreRetador,nombreBot,retador,enemigo,ctx,bot):
    continuar = True
    Respuesta = discord.Embed(colour = discord.Colour.gold())
    Respuesta.add_field(name = 'Descion',value = 'Resultado')
    for turno in range(1,151):
        if retador['Velocidad'] >= enemigo['Velocidad']:
            continuar = await Turno(nombreRetador,nombreBot,ctx,retador,enemigo,turno,bot,Respuesta)
            if continuar:
                continuar = await TurnoBot(nombreBot,ctx,enemigo,retador,Respuesta)
        else:
            continuar = await TurnoBot(nombreBot,ctx,enemigo,retador,Respuesta)
            if continuar:
                continuar = await Turno(nombreRetador,nombreBot,ctx,retador,enemigo,turno,bot,Respuesta)
        if not continuar:
            break

async def TurnoBot(atacante,ctx,stat,statSiguiente,Respuesta):
    Respuesta.set_author(name = atacante,icon_url = 'https://cdn.discordapp.com/attachments/803436405068922890/817940962940289085/thumb-126470.png')
    stop,effect = await Stats.Effect(stat,atacante)
    if stop:
        Respuesta.set_field_at(0,name = 'Time Stop',value = effect)
        await ctx.send(embed = Respuesta)
        return True
    if stat['Habilidad']['amount'] > 0:
        activacion = rd.randint(0,100)
        if activacion <= 45:
            cadena = ''
            if stat['Habilidad']['type'] == 'self':
                cadena = await Stats.ActivateAbility(stat,atacante)
            else:
                cadena = await Stats.TargetAbility(stat,statSiguiente,atacante,ctx.author)
            Respuesta.set_field_at(0,name = 'Habilidad',value = cadena + effect)
            await ctx.send(embed = Respuesta)
            return True
    if stat['Rango'] <= statSiguiente['position']:
        closer = rd.randint(7,10)
        statSiguiente['position'] -= closer
        Respuesta.set_field_at(0,name = 'Acercarse',value = f'**{atacante}** Te acercas **{closer} m** hacia el enemigo de manera ***Amenazadora***{effect}')
        await ctx.send(embed = Respuesta)
        return True
    victoria,cadena = await Stats.Damage(stat,statSiguiente,atacante)
    Respuesta.set_field_at(0,name = 'Ataque',value = cadena + effect)
    await ctx.send(embed = Respuesta)
    return not victoria

def setup(bot):
    bot.add_cog(Combat(bot))