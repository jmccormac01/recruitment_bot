"""
Discord bot for the recruitment channel

Based on Cait's LootBot
"""
import logging
from datetime import datetime as dt
import random
import traceback
from discord.ext import commands
import botsecrets
import static

# pylint: disable=invalid-name

# initialise the bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
                   description=static.description,
                   pm_help=True)

# set up logging
bot.logger = logging.getLogger('discord')
bot.logger.setLevel(logging.INFO)
log_filename = "{}/recruitment_bot-{}.log".format(static.log_path,
                                                  dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
handler = logging.FileHandler(filename=log_filename,
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(logging.Formatter(static.log_format))
bot.logger.addHandler(handler)

startup_extensions = ["utils"]

@bot.event
async def on_ready():
    """
    Shout when ready
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')

if __name__ == "__main__":
    bot.tasks = {}
    for extension in startup_extensions:
        try:
            bot.load_extension("modules.{}".format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            traceback.print_exc()
    random.seed()
    bot.run(botsecrets.token)
