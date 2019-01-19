"""
Discord bot for the recruitment channel

A lot of this info is taken from Caits LootBot
"""
import secrets
import static
import logging

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
                   description=static.description,
                   pm_help=True)

bot.logger = logging.getLogger('discord')
bot.logger.setLevel(logging.INFO)

handler = logging.FileHandler()

