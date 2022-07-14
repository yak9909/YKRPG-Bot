from discord.ext import commands
import traceback
import yktools


class Main(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.remove_command("help")
        self.loaded_extensions = yktools.load_cogs()
        for cogs in self.loaded_extensions:
            try:
                self.load_extension(cogs)
            except Exception as e:
                print(e)
                traceback.print_exc()

    async def on_ready(self):
        print("bot ready!!")
        print()
        print(f"name: {self.user.name}")
        print("development by やくると#8690")


if __name__ == '__main__':
    config = yktools.load_config()
    bot = Main(command_prefix=config["prefix"])
    bot.run(config["token"])
