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

demomento = ['**Eder**','**El pepe**','**El onichan**','**Un michi**','**L U I S**','<a:MORITE:806684100249124864>']

valor = [-1,0,1,2,3,4,5]
Probabilidades = [0.2,0.24,0.24,0.27,0.01,0.01,0.03]

Objetos =  {0:"Flint",
            1:"Stick",
            2:"Feather",
            3:"Golden Flint",
            4:"Diamond Stick",
            5:"Golden Feather"}

emojis = ['<:Flint:811814638639251457>','<:Stick:811814638983315497>',
'<:Feather:811814638630993920>','<:GoldenFlint:811840577901035543>',
'<:DiamondStick:811840519352221706>','<:GoldenFeather:811840519113015297>',
'<:StandArrow:811814640744529922>','<:StandArrow:811814640744529922>']

class Combat(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    

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
                Imagen = test.Fondo(nombre= nombre,nick= stand,data=pfp,values = values)
                arr = BytesIO()
                Imagen.save(arr, format='JPEG')
                arr.seek(0)
                await ctx.send(file = discord.File(arr, 'Stats.png'))
                arr.close()


    @commands.command(aliases=['A'])
    @commands.cooldown(rate = 1,per = 1.5, type = commands.BucketType.guild)
    @commands.max_concurrency(number = 5, per = commands.BucketType.guild)
    async def Ability(self,ctx):
        datos = await Info.GetInfo(ctx.author)
        if not datos:
            await ctx.reply('Debes usar primero Start para obtener un stand y usar estos comandos')
        else:
            color = discord.Colour.random()
            #info = await url.get_info()
            stand = datos[0]
            stats = datos[2]
            embedVar = discord.Embed(timestamp = ctx.message.created_at,color = color)
            embedVar.set_author(name = ctx.author,icon_url=ctx.author.avatar_url)
            embedVar.add_field(name='『Nombre Stand』',value=stand)
            embedVar.add_field(name='Nombre Habilidad',value = stats['Habilidad']['name'])
            embedVar.add_field(name='Descripcion',value = stats['Habilidad']['description'], inline=False)
            embedVar.add_field(name='Metodo de activacion',value=rd.choice(punto))
            embedVar.add_field(name='Limitacion',value='Sin limitaciones')
            embedVar.add_field(name='Rango',value= str(stats['Rango']) + ' m')
            await ctx.send(embed=embedVar)

    @commands.command()
    @commands.cooldown(rate = 1,per = 60, type = commands.BucketType.member)
    async def Combat(self,ctx):
        nombreRetador = ctx.author.name
        retador = await Info.GetInfo(ctx.author)
        if not retador:
            await ctx.send(f'{ctx.author.mention} Aun no has despertado tu stand, para hacerlo usa el comando Start')
        else:
            #stand = await url.nombre()
            NombreBot = rd.choice(demomento)
            values,Enemigo = await Stats.Estadisticas()
            stand = Enemigo['Habilidad']['name']
            await ctx.send(f'{ctx.author.mention} ¡{NombreBot} Te a retado a un duelo!')
            retadorStats = await Stats.StringStats(retador[2])
            enemigoStats = await Stats.StringStats(Enemigo)
            Inicio = discord.Embed(title = "Challenge", description = f'**{nombreRetador}** VS **{NombreBot}**',colour = discord.Colour.blurple())
            Inicio.add_field(name =  f'**『 {retador[0]} 』**', value = retadorStats)
            Inicio.add_field(name =  f'**『 {stand} 』**', value = enemigoStats)
            await ctx.send(embed = Inicio)
            await CombateBot(ctx.author.mention,NombreBot,retador[2],Enemigo,ctx,self.bot,1)
            if retador[2]['Vida'] <= 0:
                await ctx.send(f'{ctx.author.mention} No conseguiste nada de esta batalla')
            else:
                objeto = rd.choices(population = valor,weights = Probabilidades)
                await Info.GuardarObjeto(ctx.author,Objetos[objeto[0]],1)
                await ctx.send(f'Coneguiste: **1 {Objetos[objeto[0]]}** {emojis[objeto[0]]} Por ganar esta batalla')
            
        
    @commands.command()
    @commands.cooldown(rate = 1,per = 60, type = commands.BucketType.member)
    async def Challenge(self,ctx, *, member: discord.Member = None):
        if not member or member is ctx.author:
            await ctx.send('Debes mencionar a alguien para retarlo')
        else:
            nombreRetador = ctx.author.name
            nombreDesafiado = member.name
            retador = await Info.GetInfo(ctx.author)
            desafiado = await Info.GetInfo(member)
            if not retador or not desafiado:
                await ctx.send('Uno de los dos usuarios no a despertado su stand, para hacerlo utiliza Start')
            else:
                await ctx.send(f'{member.mention} ¡Te han retado a un duelo! \n¿Aceptas? yes / no')
                def check(m):
                    return m.channel == ctx.channel and m.author == member and m.content.lower() in ('yes','y','no','n')
                try:
                    msg = await self.bot.wait_for('message', timeout = 30.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Te demoraste mucho <:JojoThinking:801507786109222932>')
                else:
                    if msg.content.lower() in ('no','n'):
                        await ctx.send('El duelo ha sido rechazado')
                    else:
                        #await Info.EnBatalla(ctx.author,member,True)
                        retadorStats = await Stats.StringStats(retador[2])
                        desafiadoStats = await Stats.StringStats(desafiado[2])
                        Inicio = discord.Embed(title = "Challenge", description = f'**{nombreRetador}** VS **{nombreDesafiado}**',colour = discord.Colour.dark_theme())
                        Inicio.add_field(name =  f'**『 {retador[0]} 』**', value = retadorStats)
                        Inicio.add_field(name =  f'**『 {desafiado[0]} 』**', value = desafiadoStats)
                        await ctx.send(embed = Inicio)
                        await Combate(ctx.author.mention,member.mention,retador[2],desafiado[2],ctx,self.bot,1)
                        #await Info.EnBatalla(ctx.author,member,False)
                        #combate = discord.Embed(title = f'Turno: {turno}',colour = discord.Colour.gold())

async def Combate(nombreRetador,nombreDesafiado,retador,desafiado,ctx,bot,turno):
    continuar = True
    if retador['Velocidad'] >= desafiado['Velocidad']:
        continuar = await Turno(nombreRetador,nombreDesafiado,ctx,retador,desafiado,bot)
        if continuar:
            continuar = await Turno(nombreDesafiado,nombreRetador,ctx,desafiado,retador,bot)
    else:
        continuar = await Turno(nombreDesafiado,nombreRetador,ctx,desafiado,retador,bot)
        if continuar:
            continuar = await Turno(nombreRetador,nombreDesafiado,ctx,retador,desafiado,bot)
    if continuar:
        await Combate(nombreRetador,nombreDesafiado,retador,desafiado,ctx,bot,turno + 1)

async def Turno(atacante,siguienteAtacante,ctx,stat,statSiguiente,bot):
    #combate.add_field(name = f'{member} Decide tu accion. Vida: ❤ {vidaDesafiado} ',value = 'Attack - Ability - Approach - Nigerundayo')
    #await ctx.send(embed = combate)
    await ctx.send(f'{atacante} Decide tu accion. **Tu Vida: ❤ {stat["Vida"]} \nAttack - Ability - Nigerundayo**')
    def check(m):
        return m.channel == ctx.channel and m.author.mention == atacante and  m.content.lower() in ('attack','ability','nigerundayo','approach')
    try:
        msg = await bot.wait_for('message', timeout = 20.0, check=check)
    except asyncio.TimeoutError:
        stat['Vida'] -= 50
        await ctx.send(f'{atacante} Te has demorado mucho para responder, pierdes **50 ❤**')
        if stat['Vida'] <= 0:
            await ctx.send(f'{siguienteAtacante} a ganado')
            return False
        return True
    else:
        eleccion = msg.content.lower()
        if eleccion == 'attack':
            victoria,cadena = await Stats.Damage(stat,statSiguiente,atacante)
            await ctx.send(cadena)
            return not victoria
        elif eleccion == 'ability':
            if stat['Habilidad']['amount'] > 0:
                cadena = await Stats.ActivateAbility(stat,atacante)
                await ctx.send(cadena)
            else:
                await ctx.send(f'{atacante} Ya usaste tu habilidad en esta batalla')
            return True
        else:
            await ctx.send(f'https://media1.tenor.com/images/8dcdd7d0a9459951fddac8f0f116e299/tenor.gif?itemid=15566885 \n Saliste corriendo de la batalla \n{siguienteAtacante} a ganado')
            return False

async def CombateBot(nombreRetador,nombreBot,retador,enemigo,ctx,bot,turno):
    continuar = True
    if retador['Velocidad'] >= enemigo['Velocidad']:
        continuar = await Turno(nombreRetador,nombreBot,ctx,retador,enemigo,bot)
        if continuar:
            continuar = await TurnoBot(nombreBot,ctx,enemigo,retador)
    else:
        continuar = await TurnoBot(nombreBot,ctx,enemigo,retador)
        if continuar:
            continuar = await Turno(nombreRetador,nombreBot,ctx,retador,enemigo,bot)
    if continuar:
        await CombateBot(nombreRetador,nombreBot,retador,enemigo,ctx,bot,turno + 1)

async def TurnoBot(atacante,ctx,stat,statSiguiente):
    if stat['Habilidad']['amount'] > 0:
        activacion = rd.randint(0,100)
        if activacion <= 35:
            cadena = await Stats.ActivateAbility(stat,atacante)
            await ctx.send(cadena)
            return True
    victoria,cadena = await Stats.Damage(stat,statSiguiente,atacante)
    await ctx.send(cadena)
    return not victoria

def setup(bot):
    bot.add_cog(Combat(bot))