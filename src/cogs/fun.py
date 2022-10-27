import discord
from discord.ext import commands, bridge
from random import choice, sample, randint
import asyncio
from api import get_cat_fact, get_pokemon

format = "%Y/%w/%d %H:%M:%S"

# numeros = ['9️⃣','8️⃣','7️⃣','6️⃣','5️⃣','4️⃣','3️⃣','2️⃣','1️⃣','0️⃣','__**Cagaste**__ <:AdiosEder:810161891967893525><:EderNo:803232723766214667>']
skill_numbers = ('1️⃣', '2️⃣', '3️⃣', '4️⃣')
types_emojis = {'bug': '🐞', 'dark': '🌙', 'dragon': '🐲', 'electric': '⚡', 'fairy': '✨', 'fighting': '🥊', 'fire': '🔥', 'flying': '🌪️', 'ghost': '👻',
                'grass': '🌿', 'ground': '🗿', 'ice': '❄️', 'normal': '🔘', 'poison': '☠️', 'psychic': '🧠', 'rock': '⛰️', 'steel': '🛡️', 'water': '💧'}
emojis = ('🗿', '🧻', '✂')

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(aliases=['kq', 'killerqueen'])
    async def killer_queen(self, ctx: bridge.BridgeExtContext):
        data = await get_cat_fact()
        embed = discord.Embed(title='<a:GatituQueen:808381338096762930> __Gatitu__ <a:GatituQueen:808381338096762930>',
                              description=data['fact'], color=discord.Colour.random())
        await ctx.reply(embed=embed)

    @commands.command(aliases=['j'])
    async def jotaro(self, ctx: commands.Context):
        message = await ctx.reply(f'Ping: {round(self.bot.latency, 3)} ms')
        await message.add_reaction("a:Menacing:799687232344686654")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '<a:Menacing:799687232344686654>'
        try:
            await self.bot.wait_for('reaction_add', timeout=5.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await ctx.reply('https://i.kym-cdn.com/photos/images/newsfeed/001/488/696/0e7.jpg')

    @bridge.bridge_command(aliases=['p', 'poke'])
    async def pokemon(self, ctx: bridge.BridgeExtContext, *, id: int = 0):
        if id < 0 or id > 898:
            return await ctx.reply('Esta no es una ID valida')
        elif id == 0:
            id = randint(1, 898)

        def RemoveDash(cadena):
            return cadena.replace('-', ' ')

        data = await get_pokemon(id)
        embed = discord.Embed(
            title=f"__{data['name'].capitalize()}__", color=discord.Colour.random())
        embed.add_field(name='ID', value=f'__**{id}**__')
        embed.add_field(name='Tipos', value=" - ".join(
            [f"{types_emojis[tipo['type']['name']]} - **{tipo['type']['name']}**" for tipo in data['types']]))
        embed.add_field(name='Habilidad', value=RemoveDash(
            choice(data['abilities'])['ability']['name']))

        embed.add_field(name='Movimientos', value="\n ".join([f"{skill_numbers[index]} - *{RemoveDash(move['move']['name'])}*" for index, move in enumerate(
            sample(data['moves'], k=4))]) if len(data['moves']) > 3 else '1️⃣ - *Tackle* ', inline=False)
        embed.set_image(url=data['sprites']['other']
                        ['official-artwork']['front_default'])
        await ctx.reply(embed=embed)

    @bridge.bridge_command(aliases=['cj', 'cocojumbo'])
    @commands.guild_only()
    async def coco_jumbo(self, ctx: bridge.BridgeExtContext, custom_emoji: discord.Emoji = None):
        emojis = ctx.guild.emojis
        if not custom_emoji:
            await ctx.reply(choice(emojis).url)
        elif type(custom_emoji) is discord.Emoji:
            await ctx.reply(custom_emoji.url)
        else:
            for emoji in emojis:
                if emoji.name in custom_emoji:
                    await ctx.reply(emoji.url)

    @bridge.bridge_command(aliases=['hd', 'heavensdoor'])
    async def heavens_door(self, ctx: bridge.BridgeExtContext, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        avatar_url = member.display_avatar.url
        date = f'**Discord: **{member.created_at.strftime(format)}\n**{member.guild.name}: **{member.joined_at.strftime(format)}'
        embed = discord.Embed(title='『Datos del usuario』',
                              color=member.top_role.color)
        embed.add_field(name="Nombre usuario", value=member.name)
        embed.add_field(name="Alias", value=member.nick)
        embed.add_field(name="Se unio a", value=date, inline=False)
        embed.add_field(name="Rol mas alto",
                        value=member.top_role.mention, inline=False)
        actividad = member.activity
        if not actividad:
            embed.add_field(name="Actividad", value='Ninguna', inline=False)
        else:
            embed.add_field(
                name="Actividad", value=f'{actividad.type.name} {actividad.name}', inline=False)
        embed.add_field(name="Link Avatar",
                        value=f'[Avatar]({avatar_url})', inline=False)
        embed.set_image(url=avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['b2m'])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def boy2man(self, ctx: commands.Context):
        message = await ctx.reply('**Elije:** ')
        for emoji in emojis:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and reaction.emoji in emojis

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await message.clear_reactions()
            await message.edit(content='Tengo mejores cosas que hacer')
        else:
            result = choice(emojis)
            user_choice = reaction.emoji
            if user_choice == result:
                await ctx.reply(f'{result}\n**Empate** <a:Ahhhhhh:808550987983355924>')
            elif (user_choice == '🗿' and result == '✂') or (user_choice == '🧻' and result == '🗿') or (user_choice == '✂' and result == '🧻'):
                await ctx.reply(f'{result}\nMe has **Ganado** <:Que:808553130743693332>, Que suerte tienes')
            else:
                await ctx.reply(f'{result}\nQue facil a sido **Derrotarte** <:GiornoOK:808553125643288607>')

def setup(bot):
    bot.add_cog(Fun(bot))
