import discord
from discord.ext import commands
import googletrans as gt
import random as rd
from googletrans import Translator
import asyncio
import aiohttp
import url , Info
import typing

translator = Translator()
format = "%Y/%w/%d %H:%M:%S"

Estado = {'FINISHED':'Finalizado',
          'RELEASING':'En Emision',
          'NOT_YET_RELEASED':'Aun sin emitir',
          'CANCELLED':'Cancelado',
          'HIATUS':'Pausado'}

class Fun(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['Moody','MB'])
    async def MoodyBlues(self,ctx,lang,*,oracion):
        if lang not in gt.LANGUAGES:
            await ctx.send('Watashi da koto aru, WTF')
        else:
            a = translator.translate(oracion,dest = lang)
            await ctx.send(f'*{a.text}*')

    @commands.command(aliases = ['JJ'])
    async def Joseph(self,ctx):
        message = await ctx.send('Lo proximo que diras es: ')
        def check(message):
            return message.author == ctx.author
        try:
            messageUser = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('No te puedo esperar todo el dia')
        else:
            await message.edit(content = f'Lo proximo que diras es: {messageUser.content}' )

    @commands.command(aliases=['KQueen','KQ'])
    async def KillerQueen(self,ctx):
        async with ctx.channel.typing():
            color = discord.Colour.random()
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/facts/cat") as r:
                    data = await r.json()
                    embed = discord.Embed(color=color)
                    translator = Translator()
                    a = translator.translate(data['fact'],src = 'en',dest = 'es')
                    embed.add_field(name = '<a:GatituQueen:808381338096762930> Gatitu <a:GatituQueen:808381338096762930>',value= a.text, inline=False)
                    await ctx.send(embed=embed)

    @commands.command(aliases=['BR'])
    @commands.guild_only()
    async def BohemianRhapsody(self,ctx,*,busqueda:str):
        rs = await url.Animes(busqueda = busqueda)
        resultado = rs['data']['Page']['media']
        Embed = discord.Embed(color = discord.Colour.random())
        if not resultado:
            await ctx.send(f'No se encontro nada relacionado con {busqueda}')
        else:
            a = 1
            c = ''
            for res in resultado:
                b = res['title']['english']
                if b == None:
                    b = res['title']['romaji']
                c += f'{a} - {b} \n'
                a += 1
            Embed.add_field(name = 'Animes \nPon el numero del anime que quieres ver',value = c, inline=False)
            Embed.set_author(name = ctx.author.name, icon_url= ctx.author.avatar_url)
            ctx1 = await ctx.send(embed = Embed)
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author
            try:
                msg = await self.bot.wait_for('message', timeout = 45.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('Te demoraste mucho <:JojoThinking:801507786109222932>')
            else:
                try:
                    posicion = int(msg.content) - 1
                except ValueError:
                    pass
                else:
                    if posicion < 0 or posicion >= len(resultado):
                        await ctx.send('<:JojoThinking:801507786109222932> Te equivocaste al poner el numero')
                    else:
                        eleccion = resultado[posicion]
                        if not eleccion['isAdult']:
                            await msg.delete()
                            ds = eleccion['description'].replace('<br>','').replace('<b>','').replace('<i>','').replace('</i>',' ').replace('</b>',' ')
                            descripcion = translator.translate(ds,src='en',dest = 'es').text
                            Embed.set_field_at(index = 0, name = eleccion['title']['romaji'],value = descripcion, inline=False)
                            Embed.set_image(url = eleccion['coverImage']['extraLarge'])
                            Embed.add_field(name = 'Episodios',value = eleccion['episodes'])
                            duracion = str(eleccion['duration'])
                            Embed.add_field(name = 'Duracion episodios',value = f'{duracion} m')
                            Embed.add_field(name = 'Estado',value = Estado[eleccion['status']])
                            Embed.add_field(name = 'Formato', value = eleccion['format'])
                            Valoracion = eleccion['averageScore']
                            Embed.add_field(name = 'Valoracion', value = f'{Valoracion} %')
                            Embed.add_field(name = 'Generos', value = eleccion['genres'])
                            year = eleccion['startDate']['year']
                            month = eleccion['startDate']['month']
                            day = eleccion['startDate']['day']
                            Embed.set_footer(text =  f'Fecha de emision: {day}/{month}/{year}')
                            await ctx1.edit(embed = Embed)
                        else:
                            await ctx.send('Asi te queria agarrar puerco')

    @commands.command(aliases=['J'])
    async def Jotaro(self,ctx):
        await ctx.send(f'{round(self.bot.latency, 3)} ms')
        ctx1 = await ctx.send('Dio')
        await ctx1.add_reaction("a:Menacing:799687232344686654")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '<a:Menacing:799687232344686654>'
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await ctx.send('https://i.kym-cdn.com/photos/images/newsfeed/001/488/696/0e7.jpg')
        
    @commands.command(aliases=['CJ'])
    @commands.guild_only()
    async def CocoJumbo(self,ctx,*,Emoji: typing.Union[discord.Emoji,str] = None):
        emojis = ctx.guild.emojis
        if not Emoji:
            await ctx.send(rd.choice(emojis))
        elif type(Emoji) is discord.Emoji:
            await ctx.send(Emoji.url)
        else:
            for emoji in emojis:
                if emoji.name in Emoji:
                    await ctx.send(emoji.url)

    @commands.command(aliases=['HD'])
    async def HeavensDoor(self,ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        userAvatar = member.avatar_url
        datos = await Info.GetInfo(member)
        stand = 'N/A'
        NStand = 'N/A'
        if not datos:
            stand = 'Aun no ha activado el Stand'
            NStand = 'Sin Stand'
        else:
            stand = datos[0]
            NStand = 'Stand'
        color = discord.Colour.random()
        Fecha = f'**Discord: **{member.created_at.strftime(format)}\n**{member.guild.name}: **{member.joined_at.strftime(format)}'
        embedVar = discord.Embed(title = NStand, description = f'**『{stand}』**', color = color)
        embedVar.add_field(name="Nombre usuario", value=member.name)
        embedVar.add_field(name="Alias", value = member.nick)
        embedVar.add_field(name="Se unio a", value = Fecha, inline=False)
        embedVar.add_field(name="Rol mas alto", value= member.top_role.mention, inline=False)
        actividad = member.activity
        if not actividad:
            embedVar.add_field(name="Actividad", value= 'Ninguna', inline=False)
        else:
            embedVar.add_field(name="Actividad", value= actividad.name, inline=False)
            embedVar.add_field(name="Url Actividad", value= f'[Actividad]({actividad.large_image_url})', inline=False)
        embedVar.set_image(url=userAvatar)
        await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(Fun(bot))