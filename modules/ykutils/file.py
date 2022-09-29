import os
import json


# config.json の読み込み
def load_config() -> dict:
    file_path = "config.json"
    # 開発者用configファイルが存在したら
    if os.path.exists("dev_config.json"):
        file_path = "dev_config.json"

    config_file = open(file_path, mode="r+", encoding="utf-8")
    return json.load(config_file)


# dataフォルダの存在確認 無ければ作る
def check_exist(dir, root="./data"):
    if dir:
        d = dir.split("/")
        dx = ""
        for x in d:
            dx += x + "/"
            if not os.path.exists(f"{root}/{dx}"):
                print(f"directory '{x}' is not found.\ncreate '{root}/{dx}'")
                os.mkdir(f"{root}/{dx}")


# dataフォルダの存在確認（デコレータ版）
def data_check(dir, root="./data"):
    def _data_check(func):
        def wrapper(*args, **kwargs):
            check_exist(dir, root)
            return func(*args, **kwargs)
        return wrapper
    return _data_check


# Code by zkr. thanks!
def update_z(ma, mb):
    ma_keys = ma.keys()
    mb_keys = mb.keys()
    
    for mb_key in mb_keys:
        if mb_key in ma_keys:
            val = mb[mb_key]
            
            if type(val) == type(ma[mb_key]) == dict:
                ma[mb_key] = update_z(ma[mb_key], val)
            else:
                ma[mb_key] = val
        else:
            ma[mb_key] = mb[mb_key]
    
    return ma
