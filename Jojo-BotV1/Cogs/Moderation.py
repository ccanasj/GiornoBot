import discord
from discord.ext import commands
import asyncio
import Info

class Moderation(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['ZW'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True,send_messages = True)
    @commands.bot_has_permissions(manage_messages = True,manage_channels = True)
    async def ZaWarudo(self,ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role,add_reactions = False, send_messages=False)
        await ctx.send('https://i.pinimg.com/originals/af/c8/7b/afc87b53146aaeaf78eaad0bb50fd8a2.gif')

    @commands.command(aliases=['SAW'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def SoftAndWet(self,ctx, member: discord.Member):
        for channel in ctx.guild.channels:
            await channel.set_permissions(member, add_reactions = False, send_messages=False)
        await ctx.send('https://i.imgur.com/fSgLRTW.gif')
        '''guild = ctx.guild
        rol = await Info.GetInfoGuild(guild = guild)
        MutedRole = guild.get_role(rol[2])
        if not MutedRole:
            await ctx.reply('Aun no se ha creado o asignado un rol para los ususarios muteados')
        else:
            await member.add_roles(MutedRole,reason = reason)
            await ctx.send('https://i.imgur.com/fSgLRTW.gif')'''

    @commands.command(aliases=['um'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def Unmute(self,ctx, member: discord.Member):
        for channel in ctx.guild.channels:
            await channel.set_permissions(member, overwrite=None)
        await ctx.send(f'{member.mention} Ya podes hablar')
        '''guild = ctx.guild
        rol = await Info.GetInfoGuild(guild = guild)
        MutedRole = guild.get_role(rol[2])
        if not MutedRole:
            await ctx.reply('Aun no se ha creado o asignado un rol para los ususarios muteados')
        else:
            await member.remove_roles(MutedRole,reason = reason)
            await ctx.send(f'{member.mention} Ya podes hablar')'''

    @commands.command(aliases=['SP'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True,send_messages = True)
    @commands.bot_has_permissions(manage_messages = True, manage_channels = True)
    async def StarPlatinum(self,ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role,add_reactions = True ,send_messages=True)
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

    @commands.command(aliases=['ChanPre'])
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def ChangePrefix(self,ctx,*,prefix):
        if len(prefix) > 6:
            await ctx.reply('Asi te queria agarrar Esteban <a:Putazos:803782108430467122>')
        else:
            await Info.SetPrefix(guild = ctx.guild,prefix = prefix)
            await ctx.reply(f'El prefijo se ha cambiado por: {prefix}')

    @commands.command(aliases=['SWC'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels = True)
    async def SetWelcomeChannel(self,ctx,channel :discord.TextChannel):
        await Info.SetChannel(guild = ctx.guild,channel = channel.id)
        await ctx.reply(f'El canal de bienvenida se ha actualizado correctamente a: {channel.mention}')

    '''@commands.command(aliases=['SMR'])
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def SetMutedRol(self,ctx,mRol):
        for rol in ctx.guild.roles:
            if mRol in rol.name or int(mRol) == rol.id:
                await Info.SetRol(guild = ctx.guild, rol = rol.id)
                await ctx.reply(f'El rol {rol.mention} ha sido asignado como el rol para lo usurios muteados')'''

    '''@commands.command(aliases=['CMR'])
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def CreateMutedRol(self,ctx,mRol):
        guild = ctx.guild
        await guild.create_role(name = mRol)
        await ctx.reply(f'Se creo el rol {mRol} para los usuarios muteados')'''
        

def setup(bot):
    bot.add_cog(Moderation(bot))