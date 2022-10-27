import discord
from time import time
from discord import option
from discord.ext import bridge, commands
from db import exists, save_item, get_inventory, save_inventory, get_user, save_stand
from ..item_manager import generate_items, inventory_to_string, crafting, trading, recipe_to_string, use
from ..item_manager import trades, items_recipes
from ..confirm_view import ConfirmView


class Items(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def check_exists(ctx):
        return await exists(ctx.author.id)

    # @commands.command(aliases=['IO'])
    # async def InfoObjects(self,ctx):
    #     embedVar = discord.Embed(title = "Informacion Objetos", color = discord.Colour.random())
    #     embedVar.add_field(name = 'Materiales',value = '❌ Nada: **13%**\n<:Flint:811814638639251457> Flint: **16%**\n<:Stick:811814638983315497> Stick: **16%**\n<:Feather:811814638630993920> Feather: **16%**\n<:GoldenFlint:811840577901035543> Golden Flint: **3%**\n<:DiamondStick:811840519352221706> Diamond Stick: **3%**\n<:GoldenFeather:811840519113015297> Golden Feather: **3%**\n<:StandMeteorite:817954014481350698> Meteorite: **30%**')
    #     embedVar.add_field(name = 'Objetos',value = '<:StandArrow:811814640744529922> **Stand Arrow:** Invocas un nuevo stand\n- 0: **20%**  - 1: **40%**  - 2: **25%**  - 3: **10%**  - 4: **4.5%**  - 5: **0.5%** -\n<:StandArrowRequiem:814300958484856864> **Stand Arrow Requiem:** Invocas un nuevo stand mas poderoso\n- 1: ** 15%**  - 2: ** 40%**  - 3: ** 30%**  - 4: ** 10%**  - 5: ** 5%** -\n<:AbilityArrow:818650694033866752> **Skill Arrow:** Cambias tu habilidad con otra al azar\n<:StonePendant:818653936448831563> **Stone Pendant:** Aumentas en **1 nivel** tu atributo mas bajo',inline = False)
    #     await ctx.send(embed = embedVar)

    @bridge.bridge_command(aliases=['EX'])
    @commands.check(check_exists)
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def explore(self, ctx: bridge.BridgeExtContext):
        item = generate_items()
        if item['amount']:
            await save_item(ctx.author.id, item['item'], item['amount'])
        await ctx.reply(item['text'])

    @bridge.bridge_command(aliases=['i', 'inv'])
    @commands.check(check_exists)
    async def inventory(self, ctx: bridge.BridgeExtContext):
        inv = await get_inventory(ctx.author.id)
        embed = discord.Embed(title='Inventario', color=discord.Color.yellow())
        embed.add_field(name='__Materiales y Consumibles__',
                        value=inventory_to_string(inv), inline=False)
        await ctx.reply(embed=embed)

    # @commands.command(aliases=['SPW'])
    # @commands.check(CheckExiste)
    # async def SpeedWagonFoundation(self,ctx):
    #     embedVar = discord.Embed(title = '**__SpeedWagon Foundation__**', color = discord.Color.blurple())
    #     embedVar.add_field(name = '<:StoneMask:814297491021103115> Stone Mask',value = '***3000*** Puntos de Reputacion', inline = False)
    #     embedVar.add_field(name = '<:RedStoneOfAja:814298072473272322> Red Stone of Aja',value = '***5000*** Puntos de Reputacion')
    #     await ctx.send(embed = embedVar)

    @bridge.bridge_command()
    async def recipes(self, ctx: bridge.BridgeExtContext):
        embed = discord.Embed(
            title="Recetas", color=discord.Colour.brand_red())
        recipe_to_string(embed)
        # embed.add_field(name = '**『 Stone Mask with the Red Stone 』**',value =' **<:StoneMask:814297491021103115> + <:RedStoneOfAja:814298072473272322> = ** <:StoneMaskWithTheRedStone:814311812068802601>',inline = False )
        # embed.add_field(name = '**『 Memory Disc 』**',value ='Algo + Otra cosa + y creo que algo mas xd = 💿',inline = False )
        # embed.set_footer(text = f'Si necesitas informacion de algun objeto usar el comando $InfoObjects')
        await ctx.reply(embed=embed)

    @commands.slash_command()
    @commands.check(check_exists)
    @option("item", description="Escoge el objeto que vas a crear", choices=items_recipes.keys())
    @option("amount", description="Ingresa la cantidad que vas a crear", min_value=1, max_value=10, default=1)
    async def craft(self, ctx: discord.ApplicationContext, item: str, amount: int):
        inv = await get_inventory(ctx.author.id)
        accept = crafting(inv, item, amount)
        if accept:
            await save_inventory(ctx.author.id, inv)
            await ctx.respond(f'Se ha creado **x{amount} {item}**')
        else:
            await ctx.respond(f'No tienes materiales suficientes para crear **{item} x{amount}**')

    @commands.slash_command()
    @commands.check(check_exists)
    @option("material", description="Escoge el objeto que vas a intercambiar", choices=trades.keys())
    @option("amount", description="Ingresa la cantidad que vas a intercambiar", min_value=1, max_value=10, default=1)
    async def trade(self, ctx: discord.ApplicationContext, material: str, amount: int):
        inv = await get_inventory(ctx.author.id)
        accept = trading(inv, material, amount)
        if accept:
            await save_inventory(ctx.author.id, inv)
            await ctx.respond(f'Has cambiado **x{10 * amount} {trades[material]}** por **x{amount} {material}**')
        else:
            await ctx.respond(f'No tienes materiales suficientes para intercambiar **{material} x{amount}**')

    @commands.slash_command()
    @commands.check(check_exists)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @option("item", description="Escoge el objeto que vas a usar", choices=items_recipes.keys())
    async def use(self, ctx: discord.ApplicationContext, item: str):
        await ctx.defer()
        user = await get_user(ctx.author.id)
        if user['inventory'][item] > 0:
            embed = discord.Embed(title=f'Has usado __*{item}*__', color=discord.Color.random())
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            result = await use(user['stand'], item, embed)
            if type(result) != str:
                if item == 'Stone Pendant':
                    return await ctx.respond(embed=embed)
                embed.description += f'\n<t:{round(time() + 15.0)}:R>'
                view = ConfirmView(ctx.author)
                view.interaction = await ctx.respond(embed=embed, view=view)
                await view.wait()
                if view.value:
                    await save_stand(ctx.author.id, result, item)
                else:
                    await save_item(ctx.author.id, item, -1)
            else:
                await ctx.respond(result)
        else:
            await ctx.respond(f'No tienes **{item}**')

    # @commands.command()
    # @commands.check(CheckExiste)
    # @commands.cooldown(rate = 1,per = 10, type = commands.BucketType.user)
    # @commands.max_concurrency(1, per = commands.BucketType.user)
    # async def Slot(self,ctx):
    #     elecciones = rd.choices(slotPrices,k = 3)
    #     mensaje = await ctx.send(f"╔═══╦═══╦═══╗\n║ {emojis[elecciones[2]]}  ║  {emojis[elecciones[0]]}  ║ {emojis[elecciones[1]]}  ║\n╚═══╩═══╩═══╝")
    #     await asyncio.sleep(0.3)
    #     for i in range(2):
    #         for prize in range(5,7):
    #             await mensaje.edit(content = f"╔═══╦═══╦═══╗\n║ {emojis[prize - 1]}  ║  {emojis[prize + 1]}  ║ {emojis[prize]}  ║\n╚═══╩═══╩═══╝")
    #             await asyncio.sleep(0.2)
    #     await mensaje.edit(content = f"╔═══╦═══╦═══╗\n║ {emojis[elecciones[0]]}  ║  {emojis[elecciones[1]]}  ║ {emojis[elecciones[2]]}  ║\n╚═══╩═══╩═══╝")
    #     recompensa = all(elem == elecciones[0] for elem in elecciones)
    #     cadena = 'Mejor suerte para la proxima'
    #     if recompensa:
    #         await db.GuardarObjeto(ctx.author.id,Objetos[elecciones[0]],1)
    #         cadena = f'🎉 Felicidades has ganado {emojis[elecciones[0]]} **{Objetos[elecciones[0]]}** 🎉'
    #     await ctx.send(cadena)


def setup(bot):
    bot.add_cog(Items(bot))
