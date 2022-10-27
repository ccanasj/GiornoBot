import discord
from .turns import player_turn, bot_turn
from .combat_manager import attack, defend, skill, skill_check


class PVECombatView(discord.ui.View):

    interaction: discord.Interaction

    def __init__(self, player: dict, bot: dict, embed: discord.Embed):
        super().__init__(timeout=30)
        self.embed = embed
        self.turn = 1
        self.battle = False
        self.player = player
        self.bot = bot
        self.text = ''

        # if attacker['stats']['velocity'] >= defender['stats']['velocity']:
        #     self.text = ''
        # else:
        #     self.text = bot_turn(defender, attacker, self.turn)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.player['user']['id']:
            return False
        return True

    async def on_timeout(self):
        await self.interaction.edit('**Tardaste mucho**', view=None)

    @discord.ui.button(label="Ataque", style=discord.ButtonStyle.primary, emoji="⚔")
    async def attack_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.text = attack(self.player, self.bot)
        await self.send_respond(interaction)

    @discord.ui.button(label="Defensa", style=discord.ButtonStyle.primary, emoji="🛡")
    async def defend_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.text = defend(self.player)
        await self.send_respond(interaction)

    @discord.ui.button(label="Habilidad", style=discord.ButtonStyle.primary, emoji="💡", disabled=True)
    async def skill_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.text = skill(self.player, self.bot)
        await self.send_respond(interaction)

    async def send_respond(self, interaction: discord.Interaction):
        self.turn += 1
        self.text += f'\n------------------------------------------------\n{bot_turn(self.bot, self.player, self.turn)}'
        if self.player['stats']['hp'] and self.bot['stats']['hp']:
            self.children[-2].disabled = 'guard' in self.player['status']
            self.children[-1].disabled = skill_check(self.player, self.turn)
            player_turn(self.player, self.bot,
                        self.turn, self.embed, self.text)
            await interaction.response.edit_message(embed=self.embed, view=self)
        else:
            self.battle = True
            self.stop()


class PVPCombatView(discord.ui.View):

    interaction: discord.Interaction

    def __init__(self, attacker: dict, defender: dict, embed: discord.Embed):
        super().__init__(timeout=30)
        self.embed = embed
        self.turn = 1
        self.battle = False
        self.text = ''

        if attacker['stats']['velocity'] >= defender['stats']['velocity']:
            self.attacker = attacker
            self.defender = defender
        else:
            self.attacker = defender
            self.defender = attacker

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.attacker['user']['id']:
            return False
        return True

    async def on_timeout(self):
        await self.interaction.edit('**Tardaste mucho se termina la batalla**', view=None)

    @discord.ui.button(label="Ataque", style=discord.ButtonStyle.primary, emoji="⚔")
    async def attack_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.text = attack(self.attacker, self.defender)
        await self.send_respond(interaction)

    @discord.ui.button(label="Defensa", style=discord.ButtonStyle.primary, emoji="🛡")
    async def defend_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.text = defend(self.attacker)
        await self.send_respond(interaction)

    @discord.ui.button(label="Habilidad", style=discord.ButtonStyle.primary, emoji="💡", disabled=True)
    async def skill_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.text = skill(self.attacker, self.defender)
        await self.send_respond(interaction)

    async def send_respond(self, interaction: discord.Interaction):
        self.turn += 1
        if self.attacker['stats']['hp'] and self.defender['stats']['hp']:
            temp = self.attacker
            self.attacker = self.defender
            self.defender = temp
            self.children[-2].disabled = 'guard' in self.attacker['status']
            self.children[-1].disabled = skill_check(self.attacker, self.turn // 2)
            player_turn(self.attacker, self.defender,
                        self.turn // 2, self.embed, self.text)
            await interaction.response.edit_message(embed=self.embed, view=self)
        else:
            self.battle = True
            self.stop()
