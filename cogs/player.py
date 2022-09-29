from typing import Literal, Union, NamedTuple
import discord
from discord import app_commands
from discord.ext import commands
import random
from modules import ykutils, ykrpg
import math


def get_indicator(length, current_hp, max_hp):
    length = 8
    active = math.ceil((current_hp/max_hp) * length)
    disable = length - active
    return f"{'🟩'*active}{'🟥'*disable} {current_hp}/{max_hp}"


class BattleEnemy(discord.ui.Button):
    def __init__(self, obj, number):
        
        self.obj = obj
        self.number = number
        
        label = f'敵{self.number+1} {get_indicator(8, self.obj.health[0], self.obj.health[1])}'
        
        if self.obj.health[0] >= self.obj.health[1] / 2.5:
            style = discord.ButtonStyle.green
        else:
            style = discord.ButtonStyle.red
        
        super().__init__(style=style, label=label, row=number)
    
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
    
        result = self.view.battle.attack(interaction.user.id, self.number)
        if result is None:
            await interaction.response.send_message(content="あなたは既に死んでいます！", ephemeral=True)
            return
        
        self.update_label()
        
        # 攻撃側
        attacker = result["obj"]["attacker"]
        
        # 敵側
        target = result["obj"]["victim"]
        target_name = target.name
        
        enemies = result["damage"]["receive"]
        
        attack_damage = result["damage"]["attack"]
        receive_total = sum([e[1] for e in enemies])
        
        log = {
            "title": "戦闘中!",
            "color": discord.Colour.from_rgb(200, 0, 0),
            "attack": [],
            "attacker": interaction.user,
            "hp": f'{attacker.health[0]}/{attacker.health[1]}',
            "enemy": []
        }
        
        log["attack"].append(f'{target_name} に **{attack_damage}** のダメージを与えた！')
        
        if result["kill"]:
            log["attack"].append(f'{target.name} を倒した！')
            self.view.remove_item(self)
            self.disabled = True
        
            if result["result"]:
                #content.append(f'')
                self.victory(log, interaction)
                log["title"] = "敵を全て倒した！"
                log["color"] = discord.Colour.from_rgb(0, 200, 0)
                await interaction.message.edit(view=self.view, embed=self.get_embed(log))
                self.view.stop()
                return

        for enemy in enemies:
            log["enemy"].append(f'{enemy[0].name} の攻撃！{interaction.user.name} は **{enemy[1]}** のダメージを受けた！')
            if result["killer"] is not None:
                if enemy[0].name == result["killer"].name:
                    log["enemy"].append(f'**{interaction.user.name} は 死んでしまった…**')
                    await interaction.message.edit(view=self.view, embed=self.get_embed(log))
                    await interaction.response.send_message(content="あなたは死んでしまいました…", ephemeral=True)
                    break
        else:
            if len(enemies) > 1:
                log["enemy"].append(f'合計 **{receive_total}** のダメージを受けた！')
            log["hp"] = f'{attacker.health[0]}/{attacker.health[1]}'
        
        await interaction.response.edit_message(view=self.view, embed=self.get_embed(log))
    
    def check_style(self):
        if self.obj.health[0] >= self.obj.health[1] / 2.5:
            self.style = discord.ButtonStyle.green
        else:
            self.style = discord.ButtonStyle.red
    
    def update_label(self):
        self.label = f'敵{self.number+1} {get_indicator(8, self.obj.health[0], self.obj.health[1])}'
        self.check_style()
    
    def get_embed(self, log):
        embed = discord.Embed(title=log["title"], description=None, color=log["color"])
        embed.set_footer(text=f'{log["attacker"].name} HP: {log["hp"]}', icon_url=log["attacker"].avatar.url)
        embed.add_field(name=f'{log["attacker"].name} のターン', value='\n'.join(log["attack"]), inline=False)
        if log["enemy"]:
            embed.add_field(name="敵のターン", value='\n'.join(log["enemy"]), inline=False)
        return embed
    
    def victory(self, log, interaction: discord.Interaction):
        pass


class BattleEncounter(discord.ui.View):
    def __init__(self, user, enemy_kazu):
        super().__init__()
    
        self.battle = ykrpg.Battle(user.id, enemy_kazu)
        
        for i,e in enumerate(self.battle.enemies):
            self.add_item(BattleEnemy(e, i))


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        
    """
    @commands.command(name="battle")
    async def battle(self, ctx: commands.Context, kazu: int):
        kazu = int(kazu)
        if not 5 >= kazu >= 1:
            await ctx.reply("敵を出せる数は1～5体までです")
            return
    
        k = BattleEncounter(ctx.author.id, kazu)
        await ctx.send("a", view=k)
    """


async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerCog(bot))
    
    guild = discord.Object(908140851442618379)
    
    @bot.tree.command(guild=guild, description="YKRPGの戦闘を先行体験できます")
    @app_commands.describe(summon_num='敵の召喚数')
    async def battle(
        interaction: discord.Interaction,
        summon_num: app_commands.Range[int, 1, 5]
    ):
        k = BattleEncounter(interaction.user, summon_num)
        await interaction.response.send_message('敵が現れた！', view=k)
    
    @bot.tree.command(guild=guild, description="テストコマンド")
    @app_commands.describe(command='コマンド')
    async def test(
        interaction: discord.Interaction,
        command: Literal["status"]
    ):
        if command == "status":
            desc = ["━━━━《装備》━━━━", "🗡️武器: スライムソード", "🛡️防具: スライムアーマー", "━━━━━━━━━━━━"]
            embed = discord.Embed(title=f"{interaction.user.name} `Lv.1`", description="\n".join(desc))
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.set_author(name="ステータス", icon_url=bot.user.avatar.url)
            embed.set_footer(text="💰所持ゴールド: 1000 / 💎所持ユーモ: 0")
            add = embed.add_field
            add(name="⚔攻撃力: **5 (+2)**", value="─🗡️武器: スライムソード `(+2)`", inline=False)
            add(name="🦾防御力: **4 (+3)**", value="─🛡️防具: スライムアーマー `(+3)`", inline=False)
            add(name="👢素早さ: **3 (+2)**", value="─🛡️防具: スライムアーマー `(+2)`", inline=False)
            await interaction.response.send_message(embed=embed)
