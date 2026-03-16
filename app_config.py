# 应用配置：启动时加载、退出时保存用户选择

import os
import json

def get_config_path():
    """配置文件路径：与 main.py 同目录下的 conn_analysis_config.json"""
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "conn_analysis_config.json")


def load_config():
    """加载配置，若文件不存在或格式错误则返回空字典。"""
    path = get_config_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_config(config):
    """将配置字典保存为 JSON 文件。"""
    path = get_config_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except IOError:
        pass
