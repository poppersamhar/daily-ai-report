import feedparser
import requests
import re
import os
from .base import BaseFetcher, FetchedItem


class YouTubeFetcher(BaseFetcher):
    """YouTube/播客数据获取"""

    name = "youtube"
    name_zh = "YouTube/播客"
    icon = "🎬"
    color = "#ff0000"

    # 频道配置
    CHANNELS = {
        "UCSHZKyawb77ixDdsGog4iWA": "Lex Fridman",
        "UCbfYPyITQ-7l4upoX8nvctg": "Two Minute Papers",
        "UCNF5-lNi7Kqj2gYtGSz_GVQ": "AI Explained",
        "UCWN3xxRkmTPmbKwht9FuE5A": "Andrej Karpathy",
    }

    # 权重配置
    CHANNEL_WEIGHTS = {
        "Lex Fridman": 100,
        "Andrej Karpathy": 95,
        "Two Minute Papers": 85,
        "AI Explained": 80,
    }

    ENTITY_WEIGHTS = {
        "openai": 50, "gpt-5": 50, "gpt-4": 40, "gpt": 30,
        "anthropic": 45, "claude": 45,
        "google": 40, "deepmind": 40, "gemini": 40,
        "nvidia": 35, "meta": 30,
        "sam altman": 50, "altman": 40,
        "andrej karpathy": 45, "karpathy": 40,
        "dario amodei": 40, "amodei": 35,
        "jensen huang": 35, "ilya sutskever": 45,
        "scaling": 25, "transformer": 25, "agent": 25, "sota": 30,
    }

    ENTITY_PATTERNS = [
        (r"openai", "OpenAI", "company"),
        (r"gpt-?[45o]", "GPT", "company"),
        (r"anthropic", "Anthropic", "company"),
        (r"claude", "Claude", "company"),
        (r"google|deepmind|gemini", "Google", "company"),
        (r"nvidia", "NVIDIA", "company"),
        (r"meta\s*ai|llama", "Meta AI", "company"),
        (r"sam\s*altman", "Sam Altman", "person"),
        (r"karpathy", "Karpathy", "person"),
        (r"dario", "Dario Amodei", "person"),
        (r"jensen", "Jensen Huang", "person"),
        (r"ilya", "Ilya Sutskever", "person"),
    ]

    MAX_DURATION_SECONDS = 30 * 60  # 30分钟

    def __init__(self):
        super().__init__()
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY", "")

    def fetch(self) -> list[FetchedItem]:
        """获取所有频道的视频"""
        self.items = []

        for channel_id, channel_name in self.CHANNELS.items():
            print(f"  获取频道: {channel_name}")
            entries = self._fetch_rss(channel_id)

            for entry in entries:
                pub_date = entry.get("published", "")
                if not self.is_within_hours(pub_date, 24):
                    continue

                video_id = entry.get("yt_videoid", "")
                if not video_id:
                    continue

                # 获取时长
                duration_seconds = self._get_duration(video_id)

                # 过滤超长视频
                if duration_seconds > self.MAX_DURATION_SECONDS:
                    print(f"    跳过超长视频: {entry.get('title', '')[:30]}...")
                    continue

                item = FetchedItem(
                    id=video_id,
                    title=entry.get("title", ""),
                    link=entry.get("link", ""),
                    source=channel_name,
                    author=channel_name,
                    pub_date=pub_date,
                    thumbnail=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                    extra={
                        "duration_seconds": duration_seconds,
                        "duration": self._format_duration(duration_seconds),
                        "thumbnail_mq": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                    }
                )

                item.tags = self._extract_entities(item.title)
                item.fame_score = self._calculate_fame_score(item)

                self.items.append(item)
                print(f"    + {item.title[:40]}...")

        # 按知名度排序
        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_rss(self, channel_id: str) -> list:
        """获取 YouTube 频道 RSS"""
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            feed = feedparser.parse(url)
            return feed.entries
        except Exception as e:
            print(f"    RSS 获取失败: {e}")
            return []

    def _get_duration(self, video_id: str) -> int:
        """获取视频时长（秒）"""
        if not self.rapidapi_key:
            return 0

        url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
        }
        params = {"videoId": video_id}

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            return int(data.get("lengthSeconds", 0))
        except Exception as e:
            print(f"    获取时长失败 {video_id}: {e}")
            return 0

    @staticmethod
    def _format_duration(seconds: int) -> str:
        """格式化时长显示"""
        if seconds == 0:
            return "N/A"
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"

    def _extract_entities(self, title: str) -> list:
        """从标题提取关键实体"""
        entities = []
        title_lower = title.lower()
        seen = set()

        for pattern, label, entity_type in self.ENTITY_PATTERNS:
            if re.search(pattern, title_lower) and label not in seen:
                entities.append({"label": label, "type": entity_type})
                seen.add(label)

        return entities

    def _calculate_fame_score(self, item: FetchedItem) -> int:
        """计算知名度分数"""
        score = 0
        title_lower = item.title.lower()

        # 频道权重
        for name, weight in self.CHANNEL_WEIGHTS.items():
            if name.lower() in item.source.lower():
                score += weight
                break

        # 关键词权重
        for keyword, weight in self.ENTITY_WEIGHTS.items():
            if keyword in title_lower:
                score += weight

        return score
