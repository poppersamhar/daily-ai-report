"""
Daily AI Report - 全局配置
"""
import os

# API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")

# 时间窗口配置（小时）
TIME_WINDOWS = {
    "youtube": 24,
    "substack": 48,
    "twitter": 48,
    "products": 48,
    "business": 48,
}

# 每个模块显示的最大条目数
MAX_ITEMS = {
    "youtube": 10,
    "substack": 10,
    "twitter": 15,
    "products": 15,
    "business": 15,
}

# 模块启用配置
ENABLED_MODULES = [
    "youtube",
    "substack",
    "twitter",
    "products",
    "business",
]

# 输出目录
OUTPUT_DIR = "output"
