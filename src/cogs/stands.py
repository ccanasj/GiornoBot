import discord
from discord.ext import bridge, commands
from ..stand_manager import generate_stand, types
from db import save_player, exists, get_stand, get_stats
from ..stand_string import stand_to_string, skill_to_string
from ..graph import graph


stars = ['⭐', '⭐⭐', '⭐⭐⭐']


class Stands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command(aliases=['IS'])
    # async def InfoStands(self,ctx):
    #     embedVar = discord.Embed(title = "Informacion Stands", description = 'Una pequeña intoduccion a la mecanica de los Stands', color = discord.Colour.random())
    #     embedVar.add_field(name = 'Stands',
    #     value = '**__Atributos__**\n**- Velocidad:** Velocidad stand\n**- Poder:** Fuerza stand\n**- Potencia:** Potencia de las habilidades\n**- Precision:** Precision stand\n**- Activacion:** Cantidad de turnos reducidos para activar habilidad\n**- Rango:** Rango maximo stand\n**__Valores:__**\n Los valores de los atributos van desde 0 hasta 5 y aumentan sus respectivas estadisticas\n0 : 0%\n1 : 10%\n2 : 20%\n3 : 30%\n4 : 40%\n5 : 50%\n**__Estadisticas:__**\n- **Velocidad**: El stand que tenga la mayor velocidad atacara primero en cada turno\n- **Vida**: La vida del stand\n- **Fuerza**: La Fuerza del stand\n- **Rango**: La distancia maxima de alcanze del stand, si el stand no tiene suficiente rango para alcanzar el stand enemigo su daño se reduce un 30%\n- **Precision**: La precision de los ataque del stand, entre mas alto mas probable de acertar el ataque\n- **Activacion**: La cantidad de turnos necesarios para utilizar la habilidad de tu stand')
    #     await ctx.send(embed = embedVar)

    @bridge.bridge_command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def start(self, ctx: bridge.BridgeExtContext):
        await ctx.defer()
        exist = await exists(ctx.author.id)
        if not exist:
            embed = discord.Embed(
                title='Te ves fuerte, Espero no me decepciones', description='¡Ahora tienes un Stand!')
            embed.set_image(url='https://i.imgur.com/ee3wzUd.gif')
            embed.set_footer(
                text='Para ver tu stand utiliza el comando $Stand')
            stand = await generate_stand()
            await save_player(ctx.author.id, stand)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply('A ti ya te di una flecha asi que no me decepciones')

    @bridge.bridge_command()
    async def stand(self, ctx: bridge.BridgeExtContext, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        exist = await exists(member.id)
        if not exist:
            await ctx.reply('Debes usar primero $Start para obtener un stand y usar estos comandos')
        else:
            stand = await get_stand(member.id)
            stats, attributes = stand_to_string(stand)
            color = discord.Colour.random()
            embed = discord.Embed(
                title=f"『 {stand['name']} 』- {stars[stand['star'] - 1]}", color=color)
            embed.add_field(name="Stand Master", value=member.mention)
            embed.add_field(
                name=f'Nivel {stand["level"][0]}',
                value=f'<a:Exp:840278760678096927>: **__{((stand["level"][1] / stand["level"][2]) * 100):.2f}__** %')
            embed.add_field(name='Tipo Stand',
                            value=f'```asciidoc\n= {types[stand["type"]]} =```')
            embed.add_field(name="Estadisticas",
                            value=stats, inline=False)
            embed.add_field(name="Atributos", value=attributes, inline=False)
            embed.add_field(name=f"__{stand['skill']['name']}__",
                            value=skill_to_string(stand['skill']))
            #embed.add_field(name ="Acciones", value = f'🛡 - Defend + **{stats["acciones"]["Defend"] * 100:.0f}**%\n💨 - Hamon 🔪 + **{stats["acciones"]["Hamon"][0] * 100:.0f}**% - 🎯 + **{stats["acciones"]["Hamon"][1]}**%')
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(
                name=ctx.author, icon_url=ctx.author.display_avatar.url)
            await ctx.reply(embed=embed)

    @bridge.bridge_command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def stats(self, ctx: bridge.BridgeExtContext):
        await ctx.defer()
        stand = await get_stats(ctx.author.id)
        if not stand:
            await ctx.reply('Debes usar primero $Start para obtener un stand y usar estos comandos')
        else:
            color = discord.Color.random()
            embed = discord.Embed(
                title="Estadisticas", color=color)
            embed.add_field(name="Stand name", value=f"`{stand['name']}`")
            embed.set_author(name=ctx.author,
                                icon_url=ctx.author.display_avatar.url)

            def rgb2hex(r, g, b):
                return "#{:02x}{:02x}{:02x}".format(r, g, b)

            image = graph(stand['attributes'],
                            color=rgb2hex(*color.to_rgb()))
            chart = discord.File(image, filename="Stats.png")
            embed.set_image(url="attachment://Stats.png")
            await ctx.reply(embed=embed, file=chart)
            image.close()

    # @commands.command(aliases=['A'])
    # async def Ability(self,ctx):
    #     datos = await db.GetInfo(ctx.author.id)
    #     if not datos:
    #         await ctx.reply('Debes usar primero Start para obtener un stand y usar estos comandos')
    #     else:
    #         stand,stats, = datos[0],datos[2]
    #         embedVar = discord.Embed(title = f'『**{stand}**』',colour = discord.Color.blue())
    #         embedVar.set_author(name = ctx.author,icon_url=ctx.author.avatar_url)
    #         for habilidad in stats['Habilidades']:
    #             cadena = f"*{descriptions[habilidad['id']]['description']}*\n"
    #             if habilidad['active']:
    #                 Tipo = 'active'
    #                 for stat,value in habilidad["values"].items():
    #                     cadena += f'**{EmojisStats[stat]} - {stat}** | **{(value * 10):.1f}**%\n'
    #                 if 'effect' in habilidad:
    #                     for efecto, value in habilidad['effect'].items():
    #                         cadena += f"**{EfectosEmojis[efecto]} - {efecto}** por **{value}** Turnos\n"
    #             else:
    #                 Tipo = 'passive'
    #                 for efecto,value in habilidad["effect"].items():
    #                     cadena += f'**{EfectosEmojis[efecto]} - {efecto}** | **{(value * 10):.1f}**%\n'
    #             embedVar.add_field(name= f'『{habilidad["name"]}』',value = " ".join([cadena,f'**{Tipo}**']), inline=False)
    #         await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(Stands(bot))
