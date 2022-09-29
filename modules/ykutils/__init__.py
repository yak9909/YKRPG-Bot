import re
from .discord import *
from .file import *


# on/off のフォーマットのやつ（？）
def format_toggle(text):
    toggle_map = {
        "enable": ["enable", "on", "true"],
        "disable": ["disable", "off", "false"]
    }
    for k,v in toggle_map.items():
        for x in v:
            if text.lower() == x:
                if k == "enable":
                    return True
                elif k == "disable":
                    return False
    return None


# 文字列の中のURLを取得して返す
def find_url(text):
    url = re.findall(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', text)
    return url 
