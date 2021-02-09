import discord
from discord.ext import commands
import googletrans as gt
import random as rd
from googletrans import Translator
import asyncio
from io import BytesIO
import aiohttp
import url
import test

translator = Translator()
format = "%Y/%w/%d \n %H:%M:%S"

punto = {0: 'Con todo el cuerpo', 1: 'Con las Manos', 2: 'Pulsando un botón',
         3: 'A voluntad del usuario', 4: 'Con Un arma', 5: 'Abriendo algo',
         6: 'Frotando tu talón', 7: 'Con las Rodillas', 8: 'Cerrando los ojos',
         9: 'Mordiendo', 10: 'Con las Muñecas', 11: 'Con un chasquido',
         12: 'Hablando', 13: 'Con las piernas', 14: 'Con ganas de morir',
         15: 'Con miedo', 16: 'Usando algun objeto', 17: 'Con dolor'}

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

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate = 1,per = 2.5, type = commands.BucketType.channel)
    @commands.max_concurrency(number = 3, per = commands.BucketType.guild)
    async def Stats(self,ctx, *, member: discord.Member = None):
        async with ctx.channel.typing():
            if not member:
                member = ctx.message.author
            nombre = member.name
            stand  = await url.nombre()
            asset = member.avatar_url_as(size=256)
            pfp = BytesIO(await asset.read())
            Imagen = test.Fondo(nombre= nombre,nick= stand,data=pfp)
            arr = BytesIO()
            Imagen.save(arr, format='JPEG')
            arr.seek(0)
            await ctx.send(file = discord.File(arr, 'Stats.png'))
            arr.close()

    @commands.command(aliases=['ZH'])
    async def Zahando(self,ctx,opcion:int = 1, *, member: discord.Member = None):
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

    @commands.command(aliases=['A'])
    @commands.guild_only()
    @commands.cooldown(rate = 1,per = 1.5, type = commands.BucketType.guild)
    @commands.max_concurrency(number = 5, per = commands.BucketType.guild)
    async def Ability(self,ctx):
        color = discord.Colour.random()
        info = await url.get_info()
        embedVar = discord.Embed(timestamp = ctx.message.created_at,color = color)
        embedVar.set_author(name = ctx.author.name,icon_url=ctx.author.avatar_url)
        embedVar.add_field(name='『Nombre Stand』',value=info[0])
        embedVar.add_field(name='Nombre Habilidad',value=info[1])
        embedVar.add_field(name='Rango',value= str(rd.randint(1,130)) + ' m')
        embedVar.add_field(name='Descripcion',value=info[2], inline=False)
        embedVar.add_field(name='Metodo de activacion',value=rd.choice(punto))
        embedVar.add_field(name='Limitacion',value=info[3])
        await ctx.send(embed=embedVar)

    @commands.command()
    async def Jotaro(self,ctx):
        await ctx.message.add_reaction(":Planmalo:799402450431115287")
        ctx1 = await ctx.send('Dio')
        await ctx1.add_reaction("a:Menacing:799687232344686654")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '<:Planmalo:799402450431115287>'
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('https://i.ytimg.com/vi/t3S0PR8_C2w/maxresdefault.jpg')
        else:
            await ctx.send('https://i.kym-cdn.com/photos/images/newsfeed/001/488/696/0e7.jpg')
        

    @commands.command(aliases=['CJ'])
    @commands.guild_only()
    async def CocoJumbo(self,ctx,*,emoji : discord.Emoji = None):
        if not emoji:
            e = ctx.guild.emojis
            await ctx.send(rd.choice(e))
        else:
            await ctx.send(emoji.url)


    @commands.command()
    async def Stand(self,ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        userAvatar = member.avatar_url
        color = discord.Colour.random()
        embedVar = discord.Embed(title="Perfil", description="Posible stand master", color = color)
        embedVar.add_field(name="Nombre", value=member.name)
        embedVar.add_field(name="Alias", value=member.nick)
        embedVar.add_field(name="Se unio el", value=member.joined_at.strftime(format))
        embedVar.add_field(name="Rol mas alto", value= member.top_role)
        actividad = member.activity
        if not actividad:
            embedVar.add_field(name="Actividad", value= 'Ninguna')
        else:
            embedVar.add_field(name="Actividad", value= actividad.name)
        embedVar.set_image(url=userAvatar)
        await ctx.send(embed=embedVar)


    @commands.command(aliases=['Savatar','SA'])
    async def StandAvatar(self,ctx):
            mentions = ctx.message.mentions
            if not mentions:
                await ctx.send(ctx.author.avatar_url)
            else:
                for user in mentions:
                    userAvatar = user.avatar_url
                    await ctx.send(userAvatar)

    @commands.command(aliases = ['J'])
    async def Joseph(self,ctx):
        message = await ctx.send('Lo proximo que diras es: ')
        def check(message):
            return message.author == ctx.author
        try:
            messageUser = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('No te puedo esperara todo el dia')
        else:
            await message.edit(content = f'Lo proximo que diras es: {messageUser.content}' )

    @commands.command()
    async def Si(self,ctx):
        nombre = await url.nombre()
        await ctx.send(nombre)

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

def setup(bot):
    bot.add_cog(Fun(bot))