import discord
from datetime import timedelta
from discord.ext import bridge, commands

intents = discord.Intents.all()


class Giorno(bridge.Bot):

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("$"),
                         case_insensitive=True, intents=intents, debug_guilds=[682741795154558978])

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="JoJo's Bizarre Adventure"))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------------------')

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("No tengo permisos para usar este stand")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply('Este Stand no se puede usar en mensajes privados')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("No tienes el poder de usar este Stand")
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply('Aun no has despertado tu stand, para hacerlo pon el comando **$Start**')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.reply("Este Stand no existe o lo invocaste mal, Si necesitas ayuda pon **$help** ")
        elif isinstance(error, commands.EmojiNotFound):
            await ctx.reply("Este no es un emoji valido ")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Te has equivocado al invocar este Stand \nSi necesitas ayuda con este comando pon **$help {ctx.command}**")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply("Este no es un miembro valido")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f'Este Comando se esta recargando, Intentalo en **{timedelta(seconds = round(error.retry_after))}** ⏳')
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.reply('Acaba el comando anterior para seguir con este')
        elif isinstance(error, commands.BadArgument):
            await ctx.reply('Este no es un parametro correcto')
        else:
            await self.get_channel(1028361113743659079).send(f'**ID:** {ctx.author.id}\n**Mensaje:** {ctx.message.content}\n**Error:**\n`{error}`')
            await ctx.reply(f"Esto ya es un __**Error**__ del inutil de <@550479070601805855> que nunca hace nada bien <:AdiosEder:810161891967893525><:EderNo:803232723766214667>")
            raise error

    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("No tengo permisos para usar este stand")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.respond("No tienes el poder de usar este Stand")
        elif isinstance(error, discord.errors.CheckFailure):
            await ctx.respond('Aun no has despertado tu stand, para hacerlo pon el comando **$Start**')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.respond("Este no es un miembro valido")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f'Este Comando se esta recargando, Intentalo en **{timedelta(seconds = round(error.retry_after))}** ⏳')
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.respond('Acaba el comando anterior para seguir con este')
        elif isinstance(error, commands.EmojiNotFound):
            await ctx.respond("Este no es un emoji valido ")
        else:
            await self.get_channel(1028361113743659079).send(f'**ID:** {ctx.author.id}\n**Comando:** {ctx.command.name}\n**Error:**\n`{error}`')
            await ctx.respond(f"Esto ya es un __**Error**__ del inutil de <@550479070601805855> que nunca hace nada bien <:AdiosEder:810161891967893525><:EderNo:803232723766214667>")
            raise error
