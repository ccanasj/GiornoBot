from src import Giorno, Help
from src.helptest import MyHelp
from TOKEN import DISCORD

bot = Giorno()

cogs_list = [
    'combat',
    'fun',
    # 'test',
    'items',
    # 'moderation',
    'stands'
]

for cog in cogs_list:
    bot.load_extension(f'src.cogs.{cog}')

bot.help_command = MyHelp()

bot.run(DISCORD)
