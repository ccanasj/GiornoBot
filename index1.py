import discord
import aiohttp
import asyncio
import random as rd
from discord.ext import commands,tasks
from googletrans import Translator
import googletrans as gt
from io import BytesIO
import test
import url

punto = {0: 'Con todo el cuerpo', 1: 'Con las Manos', 2: 'Pulsando un botón',
         3: 'A voluntad del usuario', 4: 'Con Un arma', 5: 'Abriendo algo',
         6: 'Frotando tu talón', 7: 'Con las Rodillas', 8: 'Cerrando los ojos',
         9: 'Mordiendo', 10: 'Con las Muñecas', 11: 'Con un chasquido',
         12: 'Hablando', 13: 'Con las piernas', 14: 'Con ganas de morir'}

intents = discord.Intents.all()
translator = Translator()
bot = commands.Bot(command_prefix='$', case_insensitive=True,intents = intents)
bot.remove_command('help')
Idiomas = list(gt.LANGUAGES.items())
Pagina1 = Idiomas[:25]
Pagina2 = Idiomas[25:50]
Pagina3 = Idiomas[50:75]
Pagina4 = Idiomas[75:100]
Pagina5 = Idiomas[100:]
Paginas = [Pagina1,Pagina2,Pagina3,Pagina4,Pagina5]
Contenidos = []
for r in range(5):
    Contenido = discord.Embed(title = 'Idiomas')
    Contenido.set_footer(text = f'Pagina {r + 1}/5')
    for a , b in Paginas[r]:
        Contenido.add_field(name = f'**{b}**', value= a)
    Contenidos.append(Contenido)

#mensaje_borrado = None

@bot.group(invoke_without_command = True, case_insensitive = True)
async def help(ctx):
    embed = discord.Embed(color = discord.Colour.gold())
    embed.set_author(name = 'Jojo Bot comandos',icon_url = bot.user.avatar_url)
    embed.add_field(name="**__Moderacion__**", value='BitesTheDust \nEchoes \nStarPlatinum \nZaWarudo \nSoftAndWet \nUnmute (De momento xd)')
    embed.add_field(name="**__Entretenimiento__**", 
    value='Ability \nDio \nKillerQueen \nMoodyBlues \nRequiem \nStand \nStandAvatar \nStats \nZahando \nKakyoin (En progreso xd)')
    embed.set_footer(text = 'Para ver un comando en especifico pon $help <Nombre Comando>')

    await ctx.send(embed = embed)

@help.command(aliases=['Moody','MB'])
async def MoodyBlues(ctx):
    embed = discord.Embed(title = '**__MoodyBlues__**', description = 'Con este comando puedes traducir oraciones a el idioma que decidas',color = discord.Colour.blurple())
    embed.add_field(name= '**__Sintaxis__**' , value='$MoodyBlues <idioma> <Oracion> \n$Moody <idioma> <Oracion> \n$MB <idioma> <Oracion>')
    embed.set_footer(text = 'Si quieres ver los idiomas disponibles dale a la reaccion')
    a = await ctx.send(embed = embed)
    await a.add_reaction('a:rerorerore:801667358376460320')
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '<a:rerorerore:801667358376460320>'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        pass
    else:
        await a.clear_reactions()
        await a.edit(embed = Contenidos[0])
        await a.add_reaction('⬅️')
        await a.add_reaction('➡️')
        await Lenguajes(a,ctx.author,0)

async def Lenguajes(message,author,Pagina_Actual):
    def check(reaction, user):
        return user == author and str(reaction.emoji) == '➡️' or str(reaction.emoji) == '⬅️' 
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        pass
    else:
        if reaction.emoji == '➡️':
            Pagina_Actual += 1
            if Pagina_Actual == 5:
                Pagina_Actual = 0
            await message.edit(embed = Contenidos[Pagina_Actual])
            await Lenguajes(message,author,Pagina_Actual)
        elif reaction.emoji == '⬅️':
            Pagina_Actual -= 1
            if Pagina_Actual == -1:
                Pagina_Actual = 4
            await message.edit(embed = Contenidos[Pagina_Actual])
            await Lenguajes(message,author,Pagina_Actual)

@bot.command(aliases=['Moody','MB'])
async def MoodyBlues(ctx,lang,*,oracion):
    if lang not in gt.LANGUAGES:
        await ctx.send('Watashi da koto aru, WTF')
    else:
        a = translator.translate(oracion,dest = lang)
        await ctx.send(f'*{a.text}*')


@bot.command(aliases=['K'])
async def Kakyoin(ctx,*,busqueda):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://wallhaven.cc/api/v1/search?q={busqueda}') as r:
                data = await r.json()
                a = data['data'][0]
                await ctx.send(a['path'])


@bot.command(aliases=['ZW'])
@commands.has_permissions(manage_roles = True,send_messages = True)
async def ZaWarudo(ctx,*,Tiempo :int = 0):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('https://i.pinimg.com/originals/af/c8/7b/afc87b53146aaeaf78eaad0bb50fd8a2.gif')
    if Tiempo > 0:
        await asyncio.sleep(Tiempo)
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send('https://i.pinimg.com/originals/02/c6/8c/02c68c840e943c4aa2ebfdb7c8a6ea46.gif')
    if Tiempo < 0:
        await ctx.reply('No tengo el poder de manejar el tiempo negativo')


@bot.command(aliases=['SAW','Soft'])
@commands.has_permissions(manage_roles = True)
async def SoftAndWet(ctx, member: discord.Member):
    for canal in ctx.guild.text_channels:
        await canal.set_permissions(member,send_messages=False,add_reactions = False )
    await ctx.send('https://i.imgur.com/fSgLRTW.gif')


@bot.command(aliases=['um'])
@commands.has_permissions(manage_roles = True)
async def Unmute(ctx, member: discord.Member):
    for canal in ctx.guild.text_channels:
        await canal.set_permissions(member,send_messages = True,add_reactions = True )
    await ctx.send(f'{member.mention} Ya podes hablar')


@bot.command(aliases=['SP'])
@commands.has_permissions(manage_roles = True,send_messages = True)
async def StarPlatinum(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send('https://i.pinimg.com/originals/02/c6/8c/02c68c840e943c4aa2ebfdb7c8a6ea46.gif')


@bot.command()
async def Dio(ctx):
    await ctx.message.add_reaction(":Planmalo:799402450431115287")
    ctx1 = await ctx.send('Jotaro')
    await ctx1.add_reaction("a:Menacing:799687232344686654")
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '<:Planmalo:799402450431115287>'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('https://i.ytimg.com/vi/t3S0PR8_C2w/maxresdefault.jpg')
    else:
        await ctx.send('https://i.kym-cdn.com/photos/images/newsfeed/001/488/696/0e7.jpg')
    

@bot.command(aliases=['Re'])
async def Requiem(ctx):
    e = ctx.guild.emojis
    await ctx.send(rd.choice(e).url)


@bot.command()
async def Stand(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    color = discord.Colour.random()
    embedVar = discord.Embed(title="Perfil", description="Posible stand master", color = color)
    embedVar.set_image(url=userAvatar)
    embedVar.add_field(name="Stand User", value=member.name, inline=False)
    embedVar.add_field(name="Stand Name", value=member.nick, inline=False)
    embedVar.add_field(name="Stand Time", value=member.joined_at, inline=True)
    await ctx.send(embed=embedVar)


@bot.command(aliases=['Savatar','SA'])
async def StandAvatar(ctx, member: discord.Member = None, member2: discord.Member = None):
    if not member:
        member = ctx.message.author
        member2 = None
    if member2 == None:
        userAvatar = member.avatar_url
        await ctx.send(userAvatar)
    else:
        userAvatar = member.avatar_url
        await ctx.send(userAvatar)
        userAvatar2 = member2.avatar_url
        await ctx.send(userAvatar2)


@bot.command(aliases=['KQueen','KQ'])
async def KillerQueen(ctx):
    async with ctx.channel.typing():
        color = discord.Colour.random()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/cat") as r:
                data = await r.json()
                embed = discord.Embed(color=color)
                translator = Translator()
                a = translator.translate(data['fact'],src = 'en',dest = 'es')
                embed.add_field(name = 'Gatitu',value= a.text, inline=False)
                await ctx.send(embed=embed)


@bot.command(aliases=['btd'])
@commands.has_permissions(manage_messages = True)
async def BitesTheDust(ctx,numero:int = 1):
    await ctx.channel.purge(limit = numero + 1)
    await ctx.channel.send(f'{numero} Mensaje(s) ha(n) mordido el polvo' + ' https://i.pinimg.com/originals/87/9b/5e/879b5e50c9c11adc45aab6ed097943e1.gif')


@bot.command(aliases=['EC'])
@commands.has_permissions(manage_messages = True, manage_channels = True)
async def Echoes(ctx,numero:int = 0):
    await ctx.channel.edit(slowmode_delay = numero)
    await ctx.send('https://media1.tenor.com/images/75eb465558d8e2fed82366f81bece938/tenor.gif?itemid=17841933')


@bot.command()
async def Stats(ctx, *, member: discord.Member = None):
    async with ctx.channel.typing():
        if not member:
            member = ctx.message.author
        nombre = member.name
        stand  = member.nick
        if stand == None:
            stand = 'Sin stand'
        asset = member.avatar_url_as(size=256)
        pfp = BytesIO(await asset.read())
        test.Fondo(nombre= nombre,nick= stand,data=pfp)
        await ctx.send(file = discord.File('./Imagenes/XD.jpg'))
'''
@bot.command()
async def Sticky(ctx):
    if ctx.guild == mensaje_borrado.guild:
        if ctx.channel == mensaje_borrado.channel:
            embedVar = discord.Embed(timestamp = mensaje_borrado.created_at)
            embedVar.set_author(name = mensaje_borrado.author.name,icon_url=mensaje_borrado.author.avatar_url)
            embedVar.add_field(name='Mensaje borrado',value=mensaje_borrado.content)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send("No se encontro mensaje")
    else:
        await ctx.send("No se encontro mensaje")
'''

@bot.command(aliases=['ZH'])
async def Zahando(ctx,opcion, *, member: discord.Member = None):
    async with ctx.channel.typing():
        if not member:
            member = ctx.message.author
        avatar = member.avatar_url_as(format = 'png')
        if opcion == 1:
            await ctx.send("https://some-random-api.ml/canvas/gay?avatar=" + str(avatar))
        elif opcion == 2:
            await ctx.send("https://some-random-api.ml/canvas/triggered?avatar=" + str(avatar))
        elif opcion == 3:
            await ctx.send("https://some-random-api.ml/canvas/invert?avatar=" + str(avatar))
        elif opcion == 4:
            await ctx.send("https://some-random-api.ml/canvas/brightness?avatar=" + str(avatar))
        elif opcion == 5:
            await ctx.send("https://some-random-api.ml/canvas/blur?avatar=" + str(avatar))
        elif opcion == 6:
            await ctx.send("https://some-random-api.ml/canvas/glass?avatar=" + str(avatar))
        elif opcion == 7:
            await ctx.send("https://some-random-api.ml/canvas/wasted?avatar=" + str(avatar))
'''
@bot.listen()
async def on_message_delete(message):
    global mensaje_borrado
    mensaje_borrado = message
'''
@bot.command()
async def Ability(ctx):
    color = discord.Colour.random()
    info = url.get_info()
    embedVar = discord.Embed(timestamp = ctx.message.created_at,color = color)
    embedVar.set_author(name = ctx.author.name,icon_url=ctx.author.avatar_url)
    embedVar.add_field(name='Nombre Stand',value=info[0])
    embedVar.add_field(name='Nombre Habilidad',value=info[1])
    embedVar.add_field(name='Rango',value= str(rd.randint(1,130)) + ' m')
    embedVar.add_field(name='Descripcion',value=info[2], inline=False)
    embedVar.add_field(name='Metodo de activacion',value=rd.choice(punto))
    await ctx.send(embed=embedVar)

@bot.event
async def on_member_join(member):
    color = discord.Colour.random()
    embedVar = discord.Embed(color = color)
    embedVar.add_field(name='Bienvenido/a',value=f' <a:Menacing:799687232344686654> {member.mention} A decidido unirse a {member.guild.name} <a:Menacing:799687232344686654> \n y esta listo/a para una aventura bizzara')
    embedVar.set_image(url= 'https://media1.tenor.com/images/392da4650dfa83b3055069e39ad74b45/tenor.gif?itemid=7319727')
    await member.guild.text_channels[0].send(embed=embedVar)
          
@bot.event
async def on_member_remove(member):
    color = discord.Colour.random()
    embedVar = discord.Embed(title= f'{member.name}, Goodbye JOJO',color = color)
    embedVar.set_image(url= 'https://media1.tenor.com/images/65ae270df87c3c4adcea997e48f60852/tenor.gif?itemid=13710195')
    await member.guild.text_channels[0].send(embed=embedVar)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.BotMissingPermissions):
        await ctx.send(f"{ctx.author.mention} No tengo permisos para usar este stand")
    elif isinstance(error,commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} No tienes el poder de usar este Stand")
        await ctx.message.delete()
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention} Este Stand no existe o lo invocaste mal")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Te has equivocado al invocar este Stand")
    elif isinstance(error,commands.MemberNotFound):
        await ctx.send(f"{ctx.author.mention} Este no es un miembro valido")
    else:
        raise error

@bot.event
async def on_ready():
    await bot.change_presence(activity= discord.Activity(type=discord.ActivityType.watching,
                                                        name="JoJo's Bizarre Adventure"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run('Nzk5NDM3NTkxNTAxNDcxNzc0.YADkRg.yz0iONeUWdscajC-Ghr49dHcH9M')
