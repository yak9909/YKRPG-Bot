from discord.ext import commands
from modules import ykutils
import datetime
import traceback


class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def reload(self, ctx: commands.Context):
        if ykutils.discord.is_moderator(ctx.author.id):
            reload_extensions = [x for x in ykutils.discord.load_cogs()]
            loaded_extensions = {"success": [], "error": []}

            for cog in reload_extensions:
                try:
                    await self.bot.reload_extension(cog)
                    loaded_extensions["success"].append(cog)
                except Exception:
                    traceback.print_exc()
                    loaded_extensions["error"].append(cog)

            await ctx.send(
                (
                    f"{len(reload_extensions)}つのコグを再読み込みしました" +
                    (
                        f"が、そのうちの{len(loaded_extensions['error'])}つがエラーにより読み込まれませんでした"
                        if loaded_extensions["error"] else ""
                    )
                    if loaded_extensions["success"] else "コグは見つかりませんでした"
                ),
                delete_after=8
            )
        else:
            await ctx.send("開発者専用のコマンドです", delete_after=5)

    @commands.command()
    async def load(self, ctx: commands.Context):
        if ykutils.discord.is_moderator(ctx.author.id):
            new_extensions = [x for x in ykutils.discord.load_cogs() if x not in self.bot.loaded_extensions]
            loaded_extensions = {"success": [], "error": []}

            for cog in new_extensions:
                try:
                    await self.bot.load_extension(cog)
                    self.bot.loaded_extensions.append(cog)
                    loaded_extensions["success"].append(cog)
                except Exception:
                    traceback.print_exc()
                    loaded_extensions["error"].append(cog)

            await ctx.send(
                (
                    f"新しく{len(new_extensions)}つのコグが読み込まれました" +
                    (
                        f"が、そのうちの{len(loaded_extensions['error'])}つがエラーにより読み込まれませんでした"
                        if loaded_extensions["error"] else ""
                    )
                    if loaded_extensions["success"] else "新しいコグは見つかりませんでした"
                ),
                delete_after=8
            )
        else:
            await ctx.send("開発者専用のコマンドです", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))
