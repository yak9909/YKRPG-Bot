import discord
from discord.ext import commands
import random
import yktools
import math


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.group()
    async def test(self, ctx: commands.Context):
        pass

    @test.command(name="status")
    async def status_test(self, ctx: commands.Context):
        desc = ["━━━━《装備》━━━━", "🗡️武器: スライムソード", "🛡️防具: スライムアーマー", "━━━━━━━━━━━━"]
        embed = discord.Embed(title=f"{ctx.author.name} `Lv.1`", description="\n".join(desc))
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_author(name="ステータス", icon_url=self.bot.user.avatar.url)
        embed.set_footer(text="💰所持ゴールド: 1000 / 💎所持ユーモ: 0")
        add = embed.add_field
        add(name="⚔攻撃力: **5 (+2)**", value="─🗡️武器: スライムソード `(+2)`", inline=False)
        add(name="🦾防御力: **4 (+3)**", value="─🛡️防具: スライムアーマー `(+3)`", inline=False)
        add(name="👢素早さ: **3 (+2)**", value="─🛡️防具: スライムアーマー `(+2)`", inline=False)
        await ctx.send(embed=embed)

    @test.command(name="battle")
    async def battle_test(self, ctx: commands.Context):
        class Counter(discord.ui.View):
            def __init__(self):
                super().__init__()

            def get_hp(self, hp):
                return int(hp.split()[-1].split("/")[0]) if hp else 20

            def killed(self):
                kill = True
                for i in self.children:
                    if not self.get_hp(i.label) == 0:
                        kill = False
                return kill

            async def attack(self, button: discord.ui.Button, interaction: discord.Interaction, name):
                hp = self.get_hp(button.label)
                damage = random.randint(1, 5)
                hp -= damage

                bs = discord.ButtonStyle
                button.style = bs.green if hp >= 20/2.5 else bs.red

                if hp <= 0:
                    hp = 0
                    button.style = bs.grey
                    button.disabled = True

                length = 8
                active = math.ceil((hp/20) * length)
                disable = length - active
                button.label = str(f"{name} {'🟩'*active}{'🟥'*disable} {hp}/20")

                if hp == 0:
                    kill_msg = f"{interaction.user.name}は{name}を倒した！！"
                    await interaction.response.edit_message(view=self, content=kill_msg)
                    yktools.delete_message_after(3, await interaction.message.channel.send(kill_msg))
                    if self.killed():
                        await interaction.message.channel.send("敵を全て倒した！！")
                else:
                    await interaction.response.edit_message(
                        view=self,
                        content=f"{interaction.user.name}の攻撃！{name}に{damage}のダメージを与えた！"
                    )

            @discord.ui.button(label=f'敵1 {"🟩"*8} 20/20', style=discord.ButtonStyle.green)
            async def enemy1(self, button: discord.ui.Button, interaction: discord.Interaction):
                await self.attack(button, interaction, "敵1")

            @discord.ui.button(label=f'敵2 {"🟩"*8} 20/20', style=discord.ButtonStyle.green)
            async def enemy2(self, button: discord.ui.Button, interaction: discord.Interaction):
                await self.attack(button, interaction, "敵2")

            @discord.ui.button(label=f'敵3 {"🟩"*8} 20/20', style=discord.ButtonStyle.green)
            async def enemy3(self, button: discord.ui.Button, interaction: discord.Interaction):
                await self.attack(button, interaction, "敵3")

        await ctx.send("敵！！！！", view=Counter())

    @test.command(name="tst")
    async def tst(self, ctx: commands.Context):

        e1 = discord.ui.Button(style=discord.ButtonStyle.primary, label=f'敵1', id="e1")
        eh1 = discord.ui.Button(style=discord.ButtonStyle.primary, label=f'{"🟩"*8} 20/20', disabled=True)
        e2 = discord.ui.Button(style=discord.ButtonStyle.primary, label=f'敵2', id="e2")
        eh2 = discord.ui.Button(style=discord.ButtonStyle.primary, label=f'{"🟩"*8} 20/20', disabled=True)
        view = discord.ui.View().add_item(e1)
        #await ctx.send("a", view=)


def setup(bot):
    bot: commands.Bot
    bot.add_cog(PlayerCog(bot))
