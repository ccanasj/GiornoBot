import discord
from discord.ext import commands, bridge


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send('Hello!')

    @discord.slash_command()
    async def goodbye(self, ctx: discord.ApplicationContext):
        await ctx.respond('Goodbye!')

    @bridge.bridge_command()
    async def bye(self, ctx: bridge.BridgeExtContext):
        await ctx.respond("Bye!")

    # @discord.user_command()
    # async def greet(self, ctx, member: discord.Member):
    #     await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}!')


def setup(bot):
    bot.add_cog(Test(bot))
