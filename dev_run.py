import main
from modules import yktool
import discord


config = yktool.load_config()
bot = main.Main(command_prefix=config["prefix"])
bot.run(config["token"])
