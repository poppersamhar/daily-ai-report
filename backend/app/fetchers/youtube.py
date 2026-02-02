import feedparser
import re
import os
from .base import BaseFetcher, FetchedItem

# 尝试导入 yt-dlp
try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False


class YouTubeFetcher(BaseFetcher):
    """YouTube 播客数据获取 - 从频道 RSS 抓取"""

    name = "youtube"
    name_zh = "播客"
    icon = "🎙️"
    color = "#ff0000"

    # YouTube 频道 (channel_id -> channel_name)
    # 注意：只选择主要发布长视频/播客的频道
    CHANNELS = {
        "UCNJ1Ymd5yFuUPtn21xtRbbw": "AI Explained",
        "UCSHZKyawb77ixDdsGog4iWA": "Lex Fridman",
        "UCcefcZRL2oaA_uBNeo5UOWg": "Y Combinator",
    }

    CHANNEL_WEIGHTS = {
        "AI Explained": 95,
        "Lex Fridman": 100,
        "Y Combinator": 85,
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

    def __init__(self):
        super().__init__()
        try:
            from app.config import get_settings
            self.rapidapi_key = get_settings().rapidapi_key
        except:
            self.rapidapi_key = os.getenv("RAPIDAPI_KEY", "")

        # yt-dlp 配置
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'cookiesfrombrowser': ('chrome',),
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }

    def _get_video_duration(self, video_id: str) -> tuple[int, str]:
        """使用 yt-dlp 获取视频时长"""
        if not HAS_YTDLP:
            return 0, "N/A"

        try:
            url = f'https://www.youtube.com/watch?v={video_id}'
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False, process=False)
                if info:
                    duration_seconds = info.get('duration', 0) or 0
                    duration_str = self._format_duration(duration_seconds)
                    return duration_seconds, duration_str
        except Exception as e:
            print(f"    获取时长失败 ({video_id}): {e}")

        return 0, "N/A"

    def fetch(self) -> list[FetchedItem]:
        self.items = []

        for channel_id, channel_name in self.CHANNELS.items():
            print(f"  获取频道: {channel_name}")
            videos = self._fetch_channel_rss(channel_id, channel_name)

            for video in videos:
                pub_date = video.get("pub_date", "")
                if not self.is_within_hours(pub_date, 168):  # 7天内
                    continue

                video_id = video.get("video_id", "")
                if not video_id:
                    continue

                # 使用 yt-dlp 获取视频时长
                duration_seconds, duration_str = self._get_video_duration(video_id)

                # 过滤时长小于10分钟的视频（如果能获取到时长）
                if duration_seconds > 0 and duration_seconds < 600:  # 10分钟 = 600秒
                    print(f"    跳过短视频: {video.get('title', '')[:30]}... ({duration_seconds}s)")
                    continue

                item = FetchedItem(
                    id=video_id,
                    title=video.get("title", ""),
                    link=f"https://www.youtube.com/watch?v={video_id}",
                    source=channel_name,
                    author=channel_name,
                    pub_date=pub_date,
                    thumbnail=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                    summary="",
                    extra={
                        "duration": duration_str,
                        "duration_seconds": duration_seconds,
                        "thumbnail_mq": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                        "description": video.get("description", ""),
                    }
                )

                item.tags = self._extract_entities(item.title)
                item.fame_score = self._calculate_fame_score(item)

                self.items.append(item)
                print(f"    + {item.title[:40]}... ({duration_str})")

        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_channel_rss(self, channel_id: str, channel_name: str) -> list:
        """通过频道 RSS 获取视频"""
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            feed = feedparser.parse(url)
            videos = []
            for entry in feed.entries[:10]:
                description = ""
                if hasattr(entry, "media_group") and entry.media_group:
                    description = entry.media_group.get("media_description", "")
                elif hasattr(entry, "summary"):
                    description = entry.summary or ""

                videos.append({
                    "video_id": entry.get("yt_videoid", ""),
                    "title": entry.get("title", ""),
                    "pub_date": entry.get("published", ""),
                    "duration": "N/A",
                    "duration_seconds": 0,
                    "description": description,
                })
            return videos
        except Exception as e:
            print(f"    RSS 获取失败: {e}")
            return []

    @staticmethod
    def _format_duration(seconds: int) -> str:
        if seconds == 0:
            return "N/A"
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}:{mins:02d}:{secs:02d}"
        return f"{mins}:{secs:02d}"

    def _extract_entities(self, title: str) -> list:
        entities = []
        title_lower = title.lower()
        seen = set()

        for pattern, label, entity_type in self.ENTITY_PATTERNS:
            if re.search(pattern, title_lower) and label not in seen:
                entities.append({"label": label, "type": entity_type})
                seen.add(label)

        return entities

    def _calculate_fame_score(self, item: FetchedItem) -> int:
        score = 0
        title_lower = item.title.lower()

        for name, weight in self.CHANNEL_WEIGHTS.items():
            if name.lower() in item.source.lower():
                score += weight
                break

        for keyword, weight in self.ENTITY_WEIGHTS.items():
            if keyword in title_lower:
                score += weight

        return score
