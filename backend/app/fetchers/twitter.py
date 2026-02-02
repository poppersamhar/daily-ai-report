import requests
import os
import re
from datetime import datetime, timedelta
from .base import BaseFetcher, FetchedItem


class TwitterFetcher(BaseFetcher):
    """X/Twitter 动态数据获取"""

    name = "twitter"
    name_zh = "X"
    icon = ""
    color = "#000000"

    # 重要账号 - 用 RapidAPI 获取（稳定）
    PRIORITY_ACCOUNTS = {
        "sama": {"name": "Sam Altman", "company": "OpenAI", "priority": 1},
        "karpathy": {"name": "Andrej Karpathy", "company": "", "priority": 2},
        "ilyasut": {"name": "Ilya Sutskever", "company": "", "priority": 3},
        "DarioAmodei": {"name": "Dario Amodei", "company": "Anthropic", "priority": 4},
        "demishassabis": {"name": "Demis Hassabis", "company": "DeepMind", "priority": 5},
        "OpenAI": {"name": "OpenAI", "company": "OpenAI", "priority": 6},
        "AnthropicAI": {"name": "Anthropic", "company": "Anthropic", "priority": 7},
        "GoogleDeepMind": {"name": "Google DeepMind", "company": "Google", "priority": 8},
        "geoffreyhinton": {"name": "Geoffrey Hinton", "company": "", "priority": 9},
        "AndrewYNg": {"name": "Andrew Ng", "company": "", "priority": 10},
    }

    # AI 相关关键词（用于过滤）
    AI_KEYWORDS = [
        "ai", "gpt", "llm", "claude", "gemini", "model", "neural", "ml",
        "machine learning", "deep learning", "transformer", "agent",
        "openai", "anthropic", "deepmind", "mistral", "llama",
        "training", "inference", "benchmark", "reasoning", "agi",
        "chatbot", "assistant", "copilot", "embedding", "vector",
        "fine-tune", "prompt", "token", "parameter", "scaling",
    ]

    def __init__(self):
        super().__init__()
        # 优先从 pydantic settings 获取，否则从环境变量获取
        try:
            from app.config import get_settings
            self.rapidapi_key = get_settings().rapidapi_key
        except:
            self.rapidapi_key = os.getenv("RAPIDAPI_KEY", "")

    def fetch(self) -> list[FetchedItem]:
        """获取推文"""
        self.items = []
        all_tweets_by_account = {}

        # 1. 用 RapidAPI 获取重要账号
        print("  [RapidAPI] 获取重要账号...")
        for username, info in self.PRIORITY_ACCOUNTS.items():
            print(f"    获取: @{username} ({info['name']})")
            tweets = self._fetch_rapidapi(username)
            if tweets:
                all_tweets_by_account[username] = {
                    "info": info,
                    "tweets": tweets,
                    "source": "rapidapi"
                }

        # 2. 处理并过滤推文
        for username, data in all_tweets_by_account.items():
            info = data["info"]
            tweets = data["tweets"]

            for tweet in tweets:
                tweet_id = tweet.get("id", "")
                text = tweet.get("text", "") or tweet.get("title", "")
                created_at = tweet.get("created_at", "") or tweet.get("published", "")

                # 跳过空推文
                if not tweet_id or not text:
                    continue

                # 跳过转推
                if text.startswith("RT @"):
                    continue

                # 检查是否在48小时内
                if not self._is_recent(created_at):
                    continue

                item = FetchedItem(
                    id=tweet_id,
                    title=text[:200] if text else "",
                    link=f"https://x.com/{username}/status/{tweet_id}",
                    source=f"@{username}",
                    author=info["name"],
                    pub_date=created_at,
                    extra={
                        "username": username,
                        "company": info.get("company", ""),
                        "tweet_id": tweet_id,
                        "priority": info.get("priority", 99),
                    }
                )

                item.tags = self._extract_tags(text)
                item.fame_score = self._calculate_score(item, info)

                self.items.append(item)

        # 按发布时间排序（最新的在最上面）
        self.items.sort(key=lambda x: x.pub_date, reverse=True)
        return self.items

    def _fetch_rapidapi(self, username: str) -> list:
        """用 Twitter241 API 获取推文"""
        if not self.rapidapi_key:
            return []

        try:
            # 第一步：获取用户 ID
            user_url = "https://twitter241.p.rapidapi.com/user"
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "twitter241.p.rapidapi.com"
            }
            user_resp = requests.get(user_url, headers=headers, params={"username": username}, timeout=15)
            user_data = user_resp.json()

            user_id = user_data.get("result", {}).get("data", {}).get("user", {}).get("result", {}).get("rest_id")
            if not user_id:
                print(f"      无法获取用户ID: {username}")
                return []

            # 第二步：用用户 ID 获取推文
            tweets_url = "https://twitter241.p.rapidapi.com/user-tweets"
            tweets_resp = requests.get(tweets_url, headers=headers, params={"user": user_id, "count": "20"}, timeout=15)
            data = tweets_resp.json()

            tweets = []
            timeline = data.get("result", {}).get("timeline", {})
            instructions = timeline.get("instructions", [])

            for instruction in instructions:
                # 只处理 TimelineAddEntries 类型
                if instruction.get("type") != "TimelineAddEntries":
                    continue
                entries = instruction.get("entries", [])
                for entry in entries:
                    content = entry.get("content", {})
                    item_content = content.get("itemContent", {})
                    tweet_result = item_content.get("tweet_results", {}).get("result", {})

                    if tweet_result and tweet_result.get("__typename") == "Tweet":
                        rest_id = tweet_result.get("rest_id", "")
                        legacy = tweet_result.get("legacy", {})
                        # 获取推文文本
                        text = legacy.get("full_text", "")
                        created_at = legacy.get("created_at", "")
                        tweets.append({
                            "id": rest_id,
                            "text": text,
                            "created_at": created_at,
                        })

            print(f"      获取到 {len(tweets)} 条推文")
            return tweets

        except Exception as e:
            print(f"      RapidAPI 获取失败: {e}")
            return []

    def _is_recent(self, date_str: str) -> bool:
        """检查是否在48小时内"""
        if not date_str:
            return True  # 如果没有日期，默认保留

        try:
            from dateutil import parser
            pub_date = parser.parse(date_str)
            now = datetime.now(pub_date.tzinfo) if pub_date.tzinfo else datetime.now()
            return (now - pub_date) < timedelta(hours=168)
        except:
            return True

    def _is_ai_related(self, text: str) -> bool:
        """检查是否 AI 相关"""
        if not text:
            return False
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.AI_KEYWORDS)

    def _extract_tags(self, text: str) -> list:
        """提取标签"""
        tags = []
        text_lower = text.lower() if text else ""
        seen = set()

        tag_patterns = [
            (r"openai|gpt", "OpenAI", "company"),
            (r"anthropic|claude", "Anthropic", "company"),
            (r"google|gemini|deepmind", "Google", "company"),
            (r"meta|llama", "Meta", "company"),
            (r"mistral", "Mistral", "company"),
            (r"launch|release|announce", "发布", "event"),
            (r"agent", "Agent", "topic"),
            (r"reasoning", "Reasoning", "topic"),
        ]

        for pattern, label, tag_type in tag_patterns:
            if re.search(pattern, text_lower) and label not in seen:
                tags.append({"label": label, "type": tag_type})
                seen.add(label)

        return tags[:4]

    def _calculate_score(self, item: FetchedItem, account_info: dict) -> int:
        """计算分数"""
        score = 0
        text_lower = item.title.lower() if item.title else ""

        # 关键词权重
        keyword_weights = {
            "launch": 50, "release": 50, "announce": 45,
            "gpt": 40, "claude": 40, "gemini": 40,
            "breakthrough": 45, "sota": 40,
            "agent": 30, "reasoning": 35,
        }

        for keyword, weight in keyword_weights.items():
            if keyword in text_lower:
                score += weight

        # 优先账号加分
        priority = account_info.get("priority", 99)
        if priority <= 10:
            score += (11 - priority) * 10

        return score
