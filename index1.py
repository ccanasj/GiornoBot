import discord
import aiohttp
import asyncio
import random as rd
from discord.ext import commands
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

translator = Translator()
bot = commands.Bot(command_prefix='$', case_insensitive=True)
mensaje_borrado = None


@bot.command(aliases=['MoodyBlues','mb'])
async def moody(ctx,lang,*,oracion):
   translator = Translator()
   if lang not in gt.LANGUAGES:
      await ctx.send('Watashi da koto aru, WTF')
   else:
      a = translator.translate(oracion,dest = lang)
      await ctx.send(a.text)

@bot.command()
async def Dio(ctx):
    await ctx.message.add_reaction(":Planmalo~1:799402450431115287")
    ctx1 = await ctx.send('Jotaro')
    await ctx1.add_reaction("a:Menacing:799687232344686654")
    
@bot.command()
async def Requiem(ctx):
    e = bot.emojis
    xd = rd.randrange(len(e))
    for s in e:
        b = ":" + s.name + ":" + str(s.id)
        await ctx.message.add_reaction(b)
    #await ctx.send(bot.get_emoji(s.id).url)

@bot.command()
async def stand(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    embedVar = discord.Embed(
        title="Perfil", description="Posible stand master")
    embedVar.set_image(url=member.avatar_url)
    embedVar.add_field(name="Stand User", value=member.name, inline=False)
    embedVar.add_field(name="Stand Name", value=member.nick, inline=False)
    embedVar.add_field(name="Stand Time", value=member.joined_at, inline=True)
    await ctx.send(embed=embedVar)


@bot.command()
async def Savatar(ctx, member: discord.Member = None, member2: discord.Member = None):
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

@bot.command()
async def queen(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/facts/cat") as r:
            data = await r.json()
            embed = discord.Embed(
                title="Cat",
                color=ctx.author.color
            )
            translator = Translator()
            a = translator.translate(data['fact'],dest = 'es')
            embed.add_field(name="Gatitu", value= data['fact'], inline=False)
            await ctx.send(embed=embed)

@bot.command(aliases=['bitesthedust'])
@commands.has_permissions(manage_messages = True)
async def btd(ctx,numero:int = 1):
    await ctx.channel.purge(limit = numero + 1)
    await ctx.channel.send(f'{numero} Mensaje(s) ha(n) mordido el polvo' + ' https://i.pinimg.com/originals/87/9b/5e/879b5e50c9c11adc45aab6ed097943e1.gif')

@bot.command()
async def Stats(ctx, *, member: discord.Member = None):
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

@bot.command()
async def Zahando(ctx,opcion:int, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    avatar = member.avatar_url_as(format="png")
    if opcion == 1:
        await ctx.send("https://some-random-api.ml/canvas/gay?avatar=" + str(avatar))
    elif opcion == 2:
        await ctx.send("https://some-random-api.ml/canvas/triggered?avatar=" + str(avatar))
    elif opcion == 3:
        await ctx.send("https://some-random-api.ml/canvas/invert?avatar=" + str(avatar))
    elif opcion == 4:
        await ctx.send("https://some-random-api.ml/canvas/pixelate?avatar=" + str(avatar))
    elif opcion == 5:
        await ctx.send("https://some-random-api.ml/canvas/blur?avatar=" + str(avatar))
    elif opcion == 6:
        await ctx.send("https://some-random-api.ml/canvas/glass?avatar=" + str(avatar))
    elif opcion == 7:
        await ctx.send("https://some-random-api.ml/canvas/wasted?avatar=" + str(avatar))
    elif opcion == 8:
        await ctx.send("https://some-random-api.ml/canvas/brightness?avatar=" + str(avatar))

@bot.listen()
async def on_message_delete(message):
    global mensaje_borrado
    mensaje_borrado = message

@bot.command()
async def ability(ctx):
    info = url.get_info()
    embedVar = discord.Embed(timestamp = ctx.message.created_at)
    embedVar.set_author(name = ctx.author.name,icon_url=ctx.author.avatar_url)
    embedVar.add_field(name='Nombre Stand',value=info[0])
    embedVar.add_field(name='Nombre Habilidad',value=info[1])
    embedVar.add_field(name='Rango',value= str(rd.randint(1,130)) + ' m')
    embedVar.add_field(name='Descripcion',value=info[2], inline=False)
    embedVar.add_field(name='Metodo de activacion',value=rd.choice(punto))
    await ctx.send(embed=embedVar)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} No tienes el poder de usar este Stand")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Te has equivocado al invocar este Stand")
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

bot.run('Nzk5NDM3NTkxNTAxNDcxNzc0.YADkRg.iF0Jnh0bKoqvlf4A1fLDfAi0Q3k')
