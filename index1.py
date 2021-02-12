import discord
import asyncio
from discord.ext import commands,tasks
import datetime
import Info

async def Get_Prefix(bot,message):
   prefix = await Info.GetInfoGuild(message.guild)
   return prefix[0]

async def Get_Channel(guild):
    idChannel = await Info.GetInfoGuild(guild = guild)
    textChannel = guild.get_channel(idChannel[1])
    return textChannel

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = Get_Prefix, case_insensitive=True,intents = intents)
bot.remove_command('help')
bot.load_extension('Cogs.Help')
bot.load_extension('Cogs.Fun')
bot.load_extension('Cogs.Moderation')

'''
mensaje_borrado = None

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

@bot.listen()
async def on_message_delete(message):
    global mensaje_borrado
    mensaje_borrado = message
'''

#------------------------------------------------------------------------------------#

@bot.event
async def on_message(message):
    try:
        if message.mentions[0] == bot.user:
            pre = await Info.GetInfoGuild(message.guild)
            await message.reply(f'Mi prefijo en este server es: {pre[0]}')
    except:
        pass
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    await Info.GuardarGuild(guild = guild,prefix = '$',channel = guild.text_channels[0].id)

@bot.event
async def on_member_join(member):
    guild = member.guild
    color = discord.Colour.random()
    embedVar = discord.Embed(color = color)
    embedVar.add_field(name='Bienvenido/a',value=f' <a:Menacing:799687232344686654> {member.mention} A decidido unirse a {member.guild.name} <a:Menacing:799687232344686654> \n y esta listo/a para una aventura bizzara')
    embedVar.set_image(url= 'https://media1.tenor.com/images/392da4650dfa83b3055069e39ad74b45/tenor.gif?itemid=7319727')
    channel = await Get_Channel(guild)
    await channel.send(embed=embedVar)
          
@bot.event
async def on_member_remove(member):
    color = discord.Colour.random()
    embedVar = discord.Embed(title= f'__***Adiós***__ {member.name}',color = color)
    embedVar.set_image(url= 'https://media1.tenor.com/images/65ae270df87c3c4adcea997e48f60852/tenor.gif?itemid=13710195')
    channel = await Get_Channel(guild)
    await channel.send(embed=embedVar)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.BotMissingPermissions):
        await ctx.send(f"{ctx.author.mention} No tengo permisos para usar este stand")
    elif isinstance(error,commands.NoPrivateMessage):
        await ctx.reply('Este Stand no se puede usar en mensajes privados')
    elif isinstance(error,commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} No tienes el poder de usar este Stand")
        await ctx.message.delete()
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention} Este Stand no existe o lo invocaste mal \nSi necesitas ayuda pon $help ")
    elif isinstance(error,commands.EmojiNotFound):
        await ctx.send(f"{ctx.author.mention} Este no es un emoji valido ")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Te has equivocado al invocar este Stand \nSi necesitas ayuda con este comando pon $help {ctx.command}")
    elif isinstance(error,commands.MemberNotFound):
        await ctx.send(f"{ctx.author.mention} Este no es un miembro valido")
    elif isinstance(error,commands.CommandOnCooldown):
        await ctx.reply(f'Este Stand se esta recargando, Intentalo dentro de {datetime.timedelta(seconds = round(error.retry_after))}')
    elif isinstance(error,commands.MaxConcurrencyReached):
        await ctx.reply('Muchas personas estan usando este Stand en el server, espera un momento')
    elif isinstance(error,commands.ChannelNotFound):
        await ctx.reply('Este canal no es valido')
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