from typing import Literal, Union, NamedTuple
import discord
from discord import app_commands
from discord.ext import commands
import traceback
from modules import ykutils
import asyncio


myguild = discord.Object(908140851442618379)


class Bot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix, intents=discord.Intents.all())
        self.remove_command("help")

    async def on_ready(self):
        print("bot ready!!")
        print()
        print(f"name: {self.user.name}")
        print("development by やくると#8690")

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=myguild)


class Questionnaire(discord.ui.Modal, title='作品を審査してくださいもどき'):
    
    video = discord.ui.TextInput(label='映像点', placeholder="最大10点", max_length=2, required=True)
    audio = discord.ui.TextInput(label='音声点', placeholder="最大10点", max_length=2, required=True)
    funny = discord.ui.TextInput(label='発想点', placeholder="最大10点", max_length=2, required=True)
    
    advice = discord.ui.TextInput(label='なにかアドバイス', style=discord.TextStyle.long, required=False)
    async def on_submit(self, interaction: discord.Interaction):
        
        video = int(self.video.value)
        audio = int(self.audio.value)
        funny = int(self.funny.value)
        
        if bool([not 10 >= x >= 0 for x in [video,audio,funny] if not 10 >= x >= 0]):
            await interaction.response.send_message("0～10の点数をつけてください", ephemeral=True)
            return
        
        a = ""
        if self.advice.value:
            a = f"\n\n__**審査員からアドバイス**__\n```\n{self.advice}\n```"
        
        await interaction.response.send_message(f'映像: {video}点\n音声: {audio}点\n発想: {funny}点\n\n合計: {video+audio+funny}/30{a}')
    
    async def on_error(self, interaction: discord.Interaction, error):
        print(error)
        if isinstance(error, ValueError):
            await interaction.response.send_message("数字を入力してください", ephemeral=True)


async def main(token, prefix):
    client_bot = Bot(prefix)
    client_bot.loaded_extensions = ykutils.discord.load_cogs()
    
    for cogs in client_bot.loaded_extensions:
        try:
            await client_bot.load_extension(cogs)
        except Exception as e:
            print(e)
            traceback.print_exc()
    
    @client_bot.tree.command(guild=myguild, description="作品を審査してる感覚になれるコマンド")
    async def test_cmd(interaction: discord.Interaction):
        # Send the modal with an instance of our `Feedback` class
        # Since modals require an interaction, they cannot be done as a response to a text command.
        # They can only be done as a response to either an application command or a button press.
        await interaction.response.send_modal(Questionnaire())
            
    await client_bot.start(token=token)


if __name__ == '__main__':
    config = ykutils.file.load_config()
    asyncio.run(main(config["token"], config["prefix"]))
