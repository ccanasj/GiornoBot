import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['ZW'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True,send_messages = True)
    @commands.bot_has_permissions(manage_messages = True,manage_channels = True)
    async def ZaWarudo(self,ctx,*,Tiempo :int = 0):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send('https://i.pinimg.com/originals/af/c8/7b/afc87b53146aaeaf78eaad0bb50fd8a2.gif')
        if Tiempo > 0:
            await asyncio.sleep(Tiempo)
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send('https://i.pinimg.com/originals/02/c6/8c/02c68c840e943c4aa2ebfdb7c8a6ea46.gif')
        if Tiempo < 0:
            await ctx.reply('No tengo el poder de manejar el tiempo negativo')

    @commands.command(aliases=['SAW','Soft'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_channels = True)
    async def SoftAndWet(self,ctx, member: discord.Member):
        for canal in ctx.guild.text_channels:
            await canal.set_permissions(member,send_messages=False,add_reactions = False )
        await ctx.send('https://i.imgur.com/fSgLRTW.gif')

    @commands.command(aliases=['um'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def Unmute(self,ctx, member: discord.Member):
        for canal in ctx.guild.text_channels:
            await canal.set_permissions(member,send_messages = True,add_reactions = True )
        await ctx.send(f'{member.mention} Ya podes hablar')

    @commands.command(aliases=['SP'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True,send_messages = True)
    @commands.bot_has_permissions(manage_messages = True, manage_channels = True)
    async def StarPlatinum(self,ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send('https://i.pinimg.com/originals/02/c6/8c/02c68c840e943c4aa2ebfdb7c8a6ea46.gif')

    @commands.command(aliases=['btd'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def BitesTheDust(self,ctx,numero:int = 1):
        if numero < 1 or numero > 100:
            await ctx.send('Calmate mejor https://media.giphy.com/media/LqmUvV29Op0X1WPpRy/giphy.gif')
        else:
            await ctx.channel.purge(limit = numero + 1)
            await ctx.channel.send(f'{numero} Mensaje(s) ha(n) mordido el polvo https://i.pinimg.com/originals/87/9b/5e/879b5e50c9c11adc45aab6ed097943e1.gif')

    @commands.command(aliases=['EC'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True, manage_channels = True)
    @commands.bot_has_permissions(manage_messages = True, manage_channels = True)
    async def Echoes(self,ctx,numero:int = 0):
        await ctx.channel.edit(slowmode_delay = numero)
        await ctx.send('https://media1.tenor.com/images/75eb465558d8e2fed82366f81bece938/tenor.gif?itemid=17841933')

    @commands.command(aliases=['KC'])
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def KingCrimson(self,ctx,member: discord.Member, *, reason:str = 'Sin razon dada'):
        ctx1 = await ctx.send(f'He usado la habilidad de King Crimson y he visto como en los proximos 10 segundos eres baneado de {member.guild.name}')
        ctx2 = await ctx.send('https://64.media.tumblr.com/d94e51eba93af9499a536e50b590412b/tumblr_pt3o4ebrOm1tqvsfso3_500.gif')
        await asyncio.sleep(8)
        await ctx1.edit(content = f'{member.name} tu existencia ha sido borrada de este server')
        await ctx2.edit(content = 'https://media1.tenor.com/images/9899303e9a88ccdcb92c935568bc0e23/tenor.gif?itemid=14907260')
        await member.ban(reason = reason)

    @commands.command(aliases=['DirtyDeedsDoneDirtCheap'])
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def D4C(self,ctx,member: discord.Member, *, reason:str = 'Sin razon dada'):
        await ctx.send('https://thumbs.gfycat.com/SourPointedHackee-size_restricted.gif')
        await member.kick(reason = reason)

def setup(bot):
    bot.add_cog(Moderation(bot))