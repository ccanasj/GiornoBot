import discord
from discord.ext import commands
import googletrans as gt
import asyncio

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

class Help(commands.Cog):

    def __init__(self,bot):
        self.bot = bot 
    
    @commands.group(invoke_without_command = True, case_insensitive = True)
    async def help(self,ctx):
        embed = discord.Embed(color = discord.Colour.gold())
        embed.set_author(name = 'Giorno-Bot comandos',icon_url = self.bot.user.avatar_url)
        embed.add_field(name="**__Moderacion__**",
        value='BitesTheDust \nEchoes \nStarPlatinum \nZaWarudo \nSoftAndWet \nKingCrimson \nD4C \nUnmute (De momento xd) \nChangePrefix \nSetWelcomeChannel')
        embed.add_field(name="**__Entretenimiento__**", 
        value='Jotaro \nKillerQueen \nMoodyBlues \nCocoJumbo \nBohemianRhapsody \nJoseph \nHeavensDoor ')
        embed.add_field(name="**__Combate__**", 
        value='Combat \nChallenge')
        embed.add_field(name="**__Info Stands__**", 
        value='Start \nStand  \nStats \nAbility \nInfoStands')
        embed.add_field(name="**__Objetos__**", 
        value='Explore \nInventory \nCraft \nUse \nRecipes \nSpeedWagonFoundation \nInfoObjects')
        embed.set_footer(text = 'Para ver un comando en especifico pon [Prefijo] help <Nombre Comando>\n¡Para ver el prefijo de este server mencioname! \nLo que este entre <> es opcional, lo que este en [] es necesario completar')
        await ctx.send(embed = embed)

    @help.command(aliases=['A'])
    async def Ability(self,ctx):
        embed = discord.Embed(title = '**__Habilidad__**', description = 'Con este comando generas informacion de habilidades de Stands aleatorios',color = discord.Colour.dark_green())
        embed.add_field(name= '**__Sintaxis__**' , value='$Ability  <mencion>  \n$A  <mencion> ')
        await ctx.send(embed = embed)

    @help.command(aliases=['HD'])
    async def HeavensDoor(self,ctx):
        embed = discord.Embed(title = '**__Heaven\'sDoor__**', description = 'Este comando te da informacion del usuario ',color = discord.Colour.dark_orange())
        embed.add_field(name= '**__Sintaxis__**' , value='$HeavensDoor <mencion> \n$HD  <mencion> ')
        await ctx.send(embed = embed)
    
    @help.command(aliases = ['CJ'])
    async def CocoJumbo(self,ctx):
        embed = discord.Embed(title = '**__CocoJumbo__**', description = 'Este comando te da un emoji aleatorio del server o si pones un emoji lo hace mas grande ',color = discord.Colour.light_grey())
        embed.add_field(name= '**__Sintaxis__**' , value='$CocoJumbo  <Emoji> \n$CJ  <Emoji>')
        await ctx.send(embed = embed)
    
    @help.command()
    async def Stats(self,ctx):
        embed = discord.Embed(title = '**__Stats__**', description = 'Con este comando generas una imagen con datos del usuario y del stand',color = discord.Colour.dark_gold())
        embed.add_field(name= '**__Sintaxis__**' , value='$Stats  <mencion>')
        await ctx.send(embed = embed)
    
    @help.command(aliases=['KQ'])
    async def KillerQueen(self,ctx):
        embed = discord.Embed(title = '**__KillerQueen__**', description = '<a:GatituQueen:808381338096762930> Este comando te da datos curiosos de gatos <a:GatituQueen:808381338096762930> ',color = discord.Colour.dark_green())
        embed.add_field(name= '**__Sintaxis__**' , value='$KillerQueen \n$KQ')
        await ctx.send(embed = embed)

    @help.command(aliases = ['BR'])
    async def BohemianRhapsody(self,ctx):
        embed = discord.Embed(title = '**__BohemianRhapsody__**', description = 'Con este comando puedes buscar informacion del anime que busques',color = discord.Colour.red())
        embed.add_field(name= '**__Sintaxis__**' , value='$BohemianRhapsody  [Nombre del anime] \n$BR  [Nombre del anime]')
        await ctx.send(embed = embed)

    @help.command()
    async def Jotaro(self,ctx):
        embed = discord.Embed(title = '**__Jotaro__**', description = ' "Oh, you are approaching me???" - Algun vampiro inmortal posiblemente gei',color = discord.Colour.greyple())
        embed.add_field(name= '**__Sintaxis__**' , value='$Jotaro')
        await ctx.send(embed = embed)
    
    @help.command(aliases=['Moody','MB'])
    async def MoodyBlues(self,ctx):
        embed = discord.Embed(title = '**__MoodyBlues__**', description = 'Con este comando puedes traducir oraciones a el idioma que decidas',color = discord.Colour.blurple())
        embed.add_field(name= '**__Sintaxis__**' , value='$MoodyBlues  [idioma]  <Oracion> \n$Moody  [idioma]  <Oracion> \n$MB  [idioma]  <Oracion>')
        embed.set_footer(text = 'Si quieres ver los idiomas disponibles dale a la reaccion')
        a = await ctx.send(embed = embed)
        await a.add_reaction('a:rerorerore:801667358376460320')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '<a:rerorerore:801667358376460320>'
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await a.edit(embed = Contenidos[0])
            await a.clear_reactions()
            await a.add_reaction('⬅️')
            await a.add_reaction('➡️')
            await Lenguajes(a,ctx.author,0,self.bot)

#--------------------------------------------------------------------------
#                               Moderacion
    @help.command(aliases = ['BTD'])
    async def BitesTheDust(self,ctx):
        embed = discord.Embed(title = '**__BitesTheDust__**', description = 'Con este comando borras la cantidad de mensajes que indiques',color = discord.Colour.dark_purple())
        embed.add_field(name= '**__Sintaxis__**' , value='$BitesTheDust  <Numero de mensajes a borrar> \n$BTD  <Numero de mensajes a borrar>')
        await ctx.send(embed = embed)
    
    @help.command(aliases = ['EC'])
    async def Echoes(self,ctx):
        embed = discord.Embed(title = '**__Echoes__**', description = 'Con este comando cambias el tiempo del slowmode en el canal',color = discord.Colour.green())
        embed.add_field(name= '**__Sintaxis__**' , value='$Echoes  <Tiempo del slow> \n$EC  <Tiempo del slow>')
        embed.set_footer(text = 'Si no pones ningun numero se quitara el slowmode del canal')
        await ctx.send(embed = embed)

    @help.command(aliases = ['SP'])
    async def StarPlatinum(self,ctx):
        embed = discord.Embed(title = '**__StarPlatinum__**', description = 'Este comando te permite abrir un canal de texto',color = discord.Colour.blurple())
        embed.add_field(name= '**__Sintaxis__**' , value='$StarPlatinum \n$SP')
        await ctx.send(embed = embed)

    @help.command(aliases = ['ZW'])
    async def ZaWarudo(self,ctx):
        embed = discord.Embed(title = '**__ZaWarudo__**', description = 'Este comando te permite cerrar un canal para lo ususarios que no posean permisos',color = discord.Colour.gold())
        embed.add_field(name= '**__Sintaxis__**' , value='$ZaWarudo  <Tiempo de cierre> \n$ZW  <Tiempo de cierre>')
        embed.set_footer(text = 'El tiempo que permanece cerrado aun lo estoy perfeccionando xd')
        await ctx.send(embed = embed)

    @help.command(aliases = ['SAW'])
    async def SoftAndWet(self,ctx):
        embed = discord.Embed(title = '**__SoftAndWet__**', description = 'Con este comando muteas a un usuario, el usuario muteado no podra escribir en ningun canal de texto',color = discord.Colour.teal())
        embed.add_field(name= '**__Sintaxis__**' , value='$SoftAndWet  [Mencion] \n$SAW  [Mencion]')
        await ctx.send(embed = embed)

    @help.command(aliases = ['KC'])
    async def KingCrimson(self,ctx):
        embed = discord.Embed(title = '**__KingCrimson__**', description = 'Con estes comando baneas al usuario mencionado del server',color = discord.Colour.dark_red())
        embed.add_field(name= '**__Sintaxis__**' , value='$KingCrimson  [Mencion] <Razón>\n$KC  [Mencion] <Razón>')
        await ctx.send(embed = embed)

    @help.command(aliases = ['DirtyDeedsDoneDirtCheap'])
    async def D4C(self,ctx):
        embed = discord.Embed(title = '**__D4C__**', description = 'Con estes comando sacas al usuario del server',color = discord.Colour.dark_gold())
        embed.add_field(name= '**__Sintaxis__**' , value='$D4C  [Mencion] <Razón> \n$DirtyDeedsDoneDirtCheap  [Mencion] <Razón>')
        await ctx.send(embed = embed)

    @help.command(aliases = ['UM'])
    async def UnMute(self,ctx):
        embed = discord.Embed(title = '**__UnMute(Sera cambiado)__**', description = 'Con estes comando desmuetas a un usuario muteado')
        embed.add_field(name= '**__Sintaxis__**' , value='$UnMute  [Mencion] \n$UM  [Mencion]')
        embed.set_footer(text = 'Denme ideas la concha de la lora')
        await ctx.send(embed = embed)


async def Lenguajes(message,author,Pagina_Actual,bot):
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
            await Lenguajes(message,author,Pagina_Actual,bot)
        elif reaction.emoji == '⬅️':
            Pagina_Actual -= 1
            if Pagina_Actual == -1:
                Pagina_Actual = 4
            await message.edit(embed = Contenidos[Pagina_Actual])
            await Lenguajes(message,author,Pagina_Actual,bot)


def setup(bot):
    bot.add_cog(Help(bot))
