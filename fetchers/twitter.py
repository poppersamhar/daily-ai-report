import requests
import os
import re
from .base import BaseFetcher, FetchedItem


class TwitterFetcher(BaseFetcher):
    """X/Twitter 动态数据获取"""

    name = "twitter"
    name_zh = "X/Twitter"
    icon = "🐦"
    color = "#1da1f2"

    # 重点关注账号
    ACCOUNTS = {
        "sama": {"name": "Sam Altman", "company": "OpenAI"},
        "kaboris": {"name": "Andrej Karpathy", "company": ""},
        "ylecun": {"name": "Yann LeCun", "company": "Meta"},
        "OpenAI": {"name": "OpenAI", "company": "OpenAI"},
        "AnthropicAI": {"name": "Anthropic", "company": "Anthropic"},
        "GoogleAI": {"name": "Google AI", "company": "Google"},
        "demaboris": {"name": "Demis Hassabis", "company": "DeepMind"},
        "ilonamodei": {"name": "Dario Amodei", "company": "Anthropic"},
    }

    # 关键词权重
    KEYWORD_WEIGHTS = {
        "launch": 50, "release": 50, "announce": 45,
        "gpt": 40, "claude": 40, "gemini": 40,
        "breakthrough": 45, "sota": 40,
        "agent": 30, "reasoning": 35,
        "open source": 35, "api": 25,
    }

    def __init__(self):
        super().__init__()
        # 可以使用 RapidAPI 的 Twitter 服务
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY", "")

    def fetch(self) -> list[FetchedItem]:
        """获取 Twitter 动态

        注意：由于 Twitter API 限制，这里提供多种获取方式：
        1. 使用 RapidAPI Twitter 服务
        2. 使用 Nitter RSS（不稳定）
        3. 手动配置的静态数据
        """
        self.items = []

        # 尝试从 Nitter 获取（免费但不稳定）
        for username, info in self.ACCOUNTS.items():
            print(f"  获取: @{username} ({info['name']})")
            tweets = self._fetch_nitter(username)

            for tweet in tweets:
                pub_date = tweet.get("published", "")
                if not self.is_within_hours(pub_date, 48):
                    continue

                item = FetchedItem(
                    id=tweet.get("id", ""),
                    title=tweet.get("title", ""),
                    link=tweet.get("link", ""),
                    source=f"@{username}",
                    author=info["name"],
                    pub_date=pub_date,
                    extra={
                        "username": username,
                        "company": info["company"],
                    }
                )

                item.tags = self._extract_tags(item.title)
                item.fame_score = self._calculate_score(item, info)

                self.items.append(item)

        # 按分数排序
        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_nitter(self, username: str) -> list:
        """从 Nitter 获取推文（RSS）"""
        # Nitter 实例列表（可能不稳定）
        nitter_instances = [
            "nitter.net",
            "nitter.privacydev.net",
            "nitter.poast.org",
        ]

        for instance in nitter_instances:
            try:
                import feedparser
                url = f"https://{instance}/{username}/rss"
                feed = feedparser.parse(url)
                if feed.entries:
                    return feed.entries
            except:
                continue

        return []

    def _fetch_rapidapi(self, username: str) -> list:
        """使用 RapidAPI 获取推文"""
        if not self.rapidapi_key:
            return []

        url = "https://twitter-api45.p.rapidapi.com/timeline.php"
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com"
        }
        params = {"screenname": username}

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            return data.get("timeline", [])
        except Exception as e:
            print(f"    RapidAPI 获取失败: {e}")
            return []

    def _extract_tags(self, text: str) -> list:
        """提取标签"""
        tags = []
        text_lower = text.lower()
        seen = set()

        tag_patterns = [
            (r"openai|gpt", "OpenAI", "company"),
            (r"anthropic|claude", "Anthropic", "company"),
            (r"google|gemini", "Google", "company"),
            (r"launch|release|announce", "发布", "event"),
            (r"agent", "Agent", "topic"),
        ]

        for pattern, label, tag_type in tag_patterns:
            if re.search(pattern, text_lower) and label not in seen:
                tags.append({"label": label, "type": tag_type})
                seen.add(label)

        return tags[:3]

    def _calculate_score(self, item: FetchedItem, account_info: dict) -> int:
        """计算推文分数"""
        score = 0
        text_lower = item.title.lower()

        # 关键词权重
        for keyword, weight in self.KEYWORD_WEIGHTS.items():
            if keyword in text_lower:
                score += weight

        # 账号权重
        account_weights = {
            "sama": 50,
            "kaboris": 45,
            "OpenAI": 40,
            "AnthropicAI": 40,
            "GoogleAI": 35,
        }
        score += account_weights.get(item.extra.get("username", ""), 20)

        return score
