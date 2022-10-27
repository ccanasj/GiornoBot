import discord


class ConfirmView(discord.ui.View):

    interaction: discord.Interaction

    def __init__(self, user: discord.User, text: str = 'Confirmado'):
        super().__init__(timeout=15)
        self.value = None
        self.text = text
        self.user = user

    async def on_timeout(self):
        if isinstance(self.interaction, discord.Interaction):
            await self.interaction.edit_original_response(content='**Tardaste mucho**', view=None)
        else:
            await self.interaction.edit('**Tardaste mucho**', view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return False
        return True

    @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=self.text, view=None)
        self.value = True
        self.stop()

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.grey)
    async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content='**Cancelado**', view=None)
        self.value = False
        self.stop()
