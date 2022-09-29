import os
import re
from .file import *


# is_moderator（語彙力不足）
def is_moderator(user_id):
    moderators_id = load_config()["moderator"]
    if user_id in moderators_id:
        return True
    return False


# cogs/ 内にある .py ファイルを返す
# 先頭に # がつくファイルは無視される
def load_cogs():
    initial_cogs = []
    for file in os.listdir("cogs/"):
        if file.startswith("#"):
            continue
        if file.endswith(".py"):
            print(f"cogs.{file.split('.')[0]}")
            initial_cogs.append(f"cogs.{file.split('.')[0]}")
    return initial_cogs


# 文字列の中のTOKENを取得して返す
def find_token(text):
    token = re.findall(r'[M-Z][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}', text)
    return token
