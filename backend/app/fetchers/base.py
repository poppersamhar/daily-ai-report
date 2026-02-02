from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta


@dataclass
class FetchedItem:
    """统一的数据项结构"""
    id: str
    title: str
    title_zh: str = ""
    summary: str = ""
    link: str = ""
    source: str = ""
    author: str = ""
    pub_date: str = ""
    thumbnail: str = ""
    tags: list = field(default_factory=list)
    fame_score: int = 0
    extra: dict = field(default_factory=dict)


class BaseFetcher(ABC):
    """数据获取基类"""

    name: str = "base"
    name_zh: str = "基础"
    icon: str = "📄"
    color: str = "#007aff"

    def __init__(self):
        self.items: list[FetchedItem] = []

    @abstractmethod
    def fetch(self) -> list[FetchedItem]:
        """获取数据，子类必须实现"""
        pass

    def get_hero(self) -> Optional[FetchedItem]:
        """获取头条内容，默认返回第一个"""
        if self.items:
            return self.items[0]
        return None

    def get_items(self, limit: int = 10) -> list[FetchedItem]:
        """获取内容列表"""
        return self.items[:limit]

    def get_summary_stats(self) -> dict:
        """获取统计摘要"""
        return {
            "total": len(self.items),
            "name": self.name,
            "name_zh": self.name_zh,
            "icon": self.icon,
        }

    @staticmethod
    def is_within_hours(date_str: str, hours: int = 24) -> bool:
        """判断是否在指定小时内"""
        try:
            from dateutil import parser
            pub_date = parser.parse(date_str)
            now = datetime.now(pub_date.tzinfo)
            return (now - pub_date) < timedelta(hours=hours)
        except:
            return False

    @staticmethod
    def time_ago(date_str: str) -> str:
        """计算时间差"""
        try:
            from dateutil import parser
            pub_date = parser.parse(date_str)
            now = datetime.now(pub_date.tzinfo)
            diff = now - pub_date
            hours = int(diff.total_seconds() / 3600)

            if hours < 1:
                return "刚刚"
            elif hours < 24:
                return f"{hours}小时前"
            else:
                return f"{hours // 24}天前"
        except:
            return ""
