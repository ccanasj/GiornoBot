import discord
from discord.ext import commands, bridge
from random import choice
from time import time
from db import exists, get_stand, save_level, get_level, get_user
from src.combat_view import PVECombatView, PVPCombatView
from ..levels import experience
from ..stand_manager import generate_stand, get_boss
from ..combat_manager import set_stands
from ..confirm_view import ConfirmView
from ..stand_string import stats_to_string


training_places = ['Entrenaste con tu stand', 'Te viste unos episodios de jojos', 'Hiciste poses amenazadoras',
                   'Te jugaste unas partidas de UNO', 'Derrotaste a un pillar men', 'Derrotaste un vampiro',
                   'Mataste a un HATER DE JOJOS <:EderNo:803232723766214667>', 'Derrotaste un zombi', 'Entrenaste en el himalaya',
                   'Entrenaste tu Hamon', 'A bailar <a:JotaroDance:808550992538894368>']

enemies = ['Vanilla Ice', 'Hol Horse', 'Anubis', 'Akira Otoishi', 'Keicho Nijimura', 'Vinegar Doppio', 'Polpo', 'Risotto Nero',
           'Gato', 'Daves', 'Crim', 'Bodoque', 'Drim', 'Codinchi', 'Ima', 'Lapis', 'Montes', 'Kaiser', 'Chino', 'Dreakr', 'Nuvon', 'Gabo', 'Korvus']


class Combat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def check_exists(ctx):
        return await exists(ctx.author.id)

    @bridge.bridge_command(aliases=['tr'])
    @commands.check(check_exists)
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def train(self, ctx: bridge.BridgeExtContext):
        stand = await get_level(ctx.author.id)
        text, query = experience(stand['level'], stand['name'], 15, 30)
        await save_level(ctx.author.id, query)
        await ctx.reply(f'***{choice(training_places)}*** y {text}')

    @bridge.bridge_command()
    @commands.check(check_exists)
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def combat(self, ctx: bridge.BridgeExtContext):
        await ctx.defer()
        player = await get_stand(ctx.author.id)
        enemy = await generate_stand()

        player['user'] = {'id': ctx.author.id, 'name': ctx.author.display_name,
                          'avatar': ctx.author.display_avatar.url}
        enemy['user'] = {'id': ctx.author.id,
                         'name': choice(enemies)}
        set_stands(player, enemy)

        stats_player = stats_to_string(player["stats"], player["type"])
        stats_enemy = stats_to_string(enemy["stats"], enemy["type"])

        embed = discord.Embed(title=f'**{player["user"]["name"]}** VS **{enemy["user"]["name"]}**',
                              description=f'<t:{round(time() + 30.0)}:R>', colour=discord.Colour.blurple())

        embed.set_author(name=f'Turno: #{1}')
        embed.add_field(name=f'『 {player["name"]} 』', value=stats_player)
        embed.add_field(name="ㅤㅤ", value="ㅤㅤ")
        embed.add_field(name=f'『 {enemy["name"]} 』', value=stats_enemy)
        embed.add_field(name='ㅤ', value='ㅤ', inline=False)
        embed.set_thumbnail(url=player['user']['avatar'])

        view = PVECombatView(player, enemy, embed)
        view.interaction = await ctx.reply(content=f'¡***{enemy["user"]["name"]}*** Te retó a un duelo!', embed=embed, view=view)

        await view.wait()
        if view.battle:
            text = f'**{player["user"]["name"]}**, *{enemy["user"]["name"]}* te dominó <:GiornoOK:808553125643288607>'
            if not enemy['stats']['hp']:
                text, query = experience(
                    player['level'], player['name'], 30, 50)
                await save_level(ctx.author.id, query)
                text = f'**{player["user"]["name"]}**, !Ganaste la batalla!\n{text}'
            await view.interaction.edit(content=text, embed=None, view=None)

    @bridge.bridge_command()
    @commands.check(check_exists)
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def challenge(self, ctx: bridge.BridgeExtContext, member: discord.Member):
        if ctx.author.id == member.id:
            return await ctx.reply(content='Estas pendedjo o que? pa que vas a pelear contigo? tremendo esquizo')
        attacker = await get_stand(ctx.author.id)
        defender = await get_stand(member.id)
        if not defender:
            return await ctx.reply(f'{member.mention} Debes usar $Start para obtener un stand y usar estos comandos')
        attacker['user'] = {'id': ctx.author.id, 'name': ctx.author.display_name,
                            'avatar': ctx.author.display_avatar.url}
        defender['user'] = {'id': member.id, 'name': member.display_name,
                            'avatar': member.display_avatar.url}
        set_stands(attacker, defender)
        faster = attacker['user'] if attacker['stats']['velocity'] >= defender['stats']['velocity'] else defender['user']
        stats_attacker = stats_to_string(attacker["stats"], attacker["type"])
        stats_defender = stats_to_string(defender["stats"], defender["type"])

        embed = discord.Embed(colour=discord.Colour.random())

        embed.set_author(
            name=f'Turno: #{0} --- Turno de: {faster["name"]}', icon_url=faster['avatar'])
        embed.add_field(name=f'『 {attacker["name"]} 』', value=stats_attacker)
        embed.add_field(name="ㅤㅤ", value="ㅤㅤ")
        embed.add_field(name=f'『 {defender["name"]} 』', value=stats_defender)
        embed.add_field(name='ㅤ', value='ㅤ', inline=False)
        embed.set_thumbnail(url=faster['avatar'])

        view = ConfirmView(member)
        view.interaction = await ctx.reply(content=f'¡Hey {member.mention}, ***{attacker["user"]["name"]}*** Te retó a un duelo!\nTiempo para contestar: <t:{round(time() + 30.0)}:R>', view=view)
        await view.wait()
        if view.value:
            view_combat = PVPCombatView(attacker, defender, embed)
            view_combat.interaction = await view.interaction.edit_original_response(embed=embed, view=view_combat)
            await view_combat.wait()
            if view_combat.battle:
                await view_combat.interaction.edit(content=await end_battle(attacker, defender), embed=None, view=None)

    @bridge.bridge_command()
    @commands.check(check_exists)
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def boss(self, ctx: bridge.BridgeExtContext):
        await ctx.defer()
        player = await get_user(ctx.author.id)
        part = player['part']
        boss = get_boss(part)
        player = player['stand']
        player['user'] = {'id': ctx.author.id, 'name': ctx.author.display_name,
                          'avatar': ctx.author.display_avatar.url}
        boss['user'] = {'id': ctx.author.id, 'name': boss['name']}
        set_stands(player, boss)

        stats_player = stats_to_string(player["stats"], player["type"])
        stats_boss = stats_to_string(boss["stats"], boss["type"])

        embed = discord.Embed(title=f'**{player["user"]["name"]}** VS **{boss["user"]["name"]}**',
                              description=f'<t:{round(time() + 30.0)}:R>',
                              colour=discord.Colour.blurple())

        embed.set_author(name=f'Turno: #{1}',
                         icon_url=player['user']['avatar'])
        embed.add_field(name=f'『 {player["name"]} 』', value=stats_player)
        embed.add_field(name="ㅤㅤ", value="ㅤㅤ")
        embed.add_field(name=f'『 {boss["name"]} 』', value=stats_boss)
        embed.add_field(name='ㅤ', value='ㅤ', inline=False)
        embed.set_thumbnail(url=player['user']['avatar'])

        view = PVECombatView(player, boss, embed)
        view.interaction = await ctx.reply(content=f'¡***{boss["user"]["name"]}*** Te esta esperando!', embed=embed, view=view)

        await view.wait()
        if view.battle:
            text = f'Que facil a sido derrotarte, no eres rival para mi **{boss["user"]["name"]}** <a:KonoDIODa:808550990139621386>'
            if not boss['stats']['hp']:
                text, query = experience(
                    player['level'], player['name'], 150*part, 200*part)
                if '$inc' in query:
                    query['$inc']['part'] = 1
                else:
                    query['$inc'] = {'part': 1}
                await save_level(ctx.author.id, query)
                text = f'No puede ser\n **{player["user"]["name"]}**, !Ganaste la batalla!\n{text}'
            await view.interaction.edit(content=text, embed=None, view=None)


async def end_battle(attacker, defender):
    if not defender['stats']['hp']:
        attacker_exp = (36, 50)
        defender_exp = (20, 35)
        text = f'**¡Gano {attacker["user"]["name"]}!** ' + \
            '{0}' + f'\n\n*{defender["user"]["name"]}*, ' + '{1}'
    else:
        attacker_exp = (20, 35)
        defender_exp = (36, 50)
        text = f'**¡Gano {defender["user"]["name"]}!** ' + \
            '{1}' + f'\n\n*{attacker["user"]["name"]}*, ' + '{0}'

    text_attacker, query = experience(
        attacker['level'], attacker['name'], attacker_exp[0], attacker_exp[1])
    await save_level(attacker["user"]["id"], query)
    text_defender, query = experience(
        defender['level'], defender['name'], defender_exp[0], defender_exp[1])
    await save_level(defender["user"]["id"], query)
    return text.format(text_attacker, text_defender)


def setup(bot):
    bot.add_cog(Combat(bot))
