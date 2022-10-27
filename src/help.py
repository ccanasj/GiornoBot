import discord
from discord.ext import commands


class Help(commands.HelpCommand):

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def send_bot_help(self, mapping):
        embed = discord.Embed(color=discord.Colour.gold())
        embed.set_author(name='Giorno-Bot comandos',
                         icon_url=self.bot.user.avatar_url)
        embed.add_field(name="💡 **__Moderacion__**",
                        value='BitesTheDust \nEchoes \nStarPlatinum \nZaWarudo \nKingCrimson \nD4C')
        embed.add_field(name="🎲 **__Entretenimiento__**",
                        value='Jotaro \nKillerQueen \nCocoJumbo \nHeavensDoor \nBoy2Man 🆕 \nPokemon 🆕')
        embed.add_field(name="⚔ **__Combate__**",
                        value='Combat  🆕 \nChallenge  🆕 \nTraining  🆕\nBoss 🆕\n Tower (Creo que ya sabes xd) ')
        embed.add_field(name="<a:GatituQueen:808381338096762930> **__Stands__**",
                        value='Start \nStand  \nStats \nAbility \nCooldowns 🆕')
        embed.add_field(name="💎 **__Objetos__**",
                        value='Explore \nInventory \nCraft \nUse \nTrade 🆕 \nSlot 🆕\nRecipes \nSWF')
        embed.add_field(name="ℹ **__Info (Aun no lo implemento xd)__**",
                        value='Stand \nStats \nAttributes \nEffects \nActions \nObjects \nItems')
        embed.add_field(name="⚙️ **__Ajustes (Algun dia xdddddd)__**",
                        value='__**W I P**__')
        embed.add_field(name="|| <:EderNo:803232723766214667> ||",
                        value='|| $Emanuel ||\n|| $Camilo ||')
        embed.set_footer(
            text='Para ver un comando en especifico pon [Prefijo] help <Nombre Comando>\nLo que este entre <> es opcional, lo que este en [] es necesario completar')
        channel = self.get_destination()
        await channel.send(embed=embed)

#     @help.command(aliases=['A'])
#     async def Ability(self, ctx):
#         embed = discord.Embed(title='**__Habilidad__**',
#                               description='Con este comando generas informacion de habilidades de Stands aleatorios', color=discord.Colour.dark_green())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$Ability  <mencion>  \n$A  <mencion> ')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['HD'])
#     async def HeavensDoor(self, ctx):
#         embed = discord.Embed(title='**__Heaven\'sDoor__**',
#                               description='Este comando te da informacion del usuario ', color=discord.Colour.dark_orange())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$HeavensDoor <mencion> \n$HD  <mencion> ')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['CJ'])
#     async def CocoJumbo(self, ctx):
#         embed = discord.Embed(title='**__CocoJumbo__**',
#                               description='Este comando te da un emoji aleatorio del server o si pones un emoji lo hace mas grande ', color=discord.Colour.light_grey())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$CocoJumbo  <Emoji> \n$CJ  <Emoji>')
#         await ctx.send(embed=embed)

#     @help.command()
#     async def Stats(self, ctx):
#         embed = discord.Embed(
#             title='**__Stats__**', description='Con este comando generas una imagen con datos del usuario y del stand', color=discord.Colour.dark_gold())
#         embed.add_field(name='**__Sintaxis__**', value='$Stats  <mencion>')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['KQ'])
#     async def KillerQueen(self, ctx):
#         embed = discord.Embed(title='**__KillerQueen__**',
#                               description='<a:GatituQueen:808381338096762930> Este comando te da datos curiosos de gatos <a:GatituQueen:808381338096762930> ', color=discord.Colour.dark_green())
#         embed.add_field(name='**__Sintaxis__**', value='$KillerQueen \n$KQ')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['BR'])
#     async def BohemianRhapsody(self, ctx):
#         embed = discord.Embed(title='**__BohemianRhapsody__**',
#                               description='Con este comando puedes buscar informacion del anime que busques', color=discord.Colour.red())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$BohemianRhapsody  [Nombre del anime] \n$BR  [Nombre del anime]')
#         await ctx.send(embed=embed)

#     @help.command()
#     async def Jotaro(self, ctx):
#         embed = discord.Embed(
#             title='**__Jotaro__**', description=' "Oh, you are approaching me???" - Algun vampiro inmortal posiblemente gei', color=discord.Colour.greyple())
#         embed.add_field(name='**__Sintaxis__**', value='$Jotaro')
#         await ctx.send(embed=embed)

# # --------------------------------------------------------------------------
# #                               Moderacion
#     @help.command(aliases=['BTD'])
#     async def BitesTheDust(self, ctx):
#         embed = discord.Embed(title='**__BitesTheDust__**',
#                               description='Con este comando borras la cantidad de mensajes que indiques', color=discord.Colour.dark_purple())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$BitesTheDust  <Numero de mensajes a borrar> \n$BTD  <Numero de mensajes a borrar>')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['EC'])
#     async def Echoes(self, ctx):
#         embed = discord.Embed(
#             title='**__Echoes__**', description='Con este comando cambias el tiempo del slowmode en el canal', color=discord.Colour.green())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$Echoes  <Tiempo del slow> \n$EC  <Tiempo del slow>')
#         embed.set_footer(
#             text='Si no pones ningun numero se quitara el slowmode del canal')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['SP'])
#     async def StarPlatinum(self, ctx):
#         embed = discord.Embed(title='**__StarPlatinum__**',
#                               description='Este comando te permite abrir un canal de texto', color=discord.Colour.blurple())
#         embed.add_field(name='**__Sintaxis__**', value='$StarPlatinum \n$SP')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['ZW'])
#     async def ZaWarudo(self, ctx):
#         embed = discord.Embed(
#             title='**__ZaWarudo__**', description='Este comando te permite cerrar un canal para lo ususarios que no posean permisos', color=discord.Colour.gold())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$ZaWarudo  <Tiempo de cierre> \n$ZW  <Tiempo de cierre>')
#         embed.set_footer(
#             text='El tiempo que permanece cerrado aun lo estoy perfeccionando xd')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['KC'])
#     async def KingCrimson(self, ctx):
#         embed = discord.Embed(title='**__KingCrimson__**',
#                               description='Con estes comando baneas al usuario mencionado del server', color=discord.Colour.dark_red())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$KingCrimson  [Mencion] <Razón>\n$KC  [Mencion] <Razón>')
#         await ctx.send(embed=embed)

#     @help.command(aliases=['DirtyDeedsDoneDirtCheap'])
#     async def D4C(self, ctx):
#         embed = discord.Embed(
#             title='**__D4C__**', description='Con estes comando sacas al usuario del server', color=discord.Colour.dark_gold())
#         embed.add_field(name='**__Sintaxis__**',
#                         value='$D4C  [Mencion] <Razón> \n$DirtyDeedsDoneDirtCheap  [Mencion] <Razón>')
#         await ctx.send(embed=embed)
