import feedparser
import re
import hashlib
from datetime import datetime, timedelta
from .base import BaseFetcher, FetchedItem


class ApplePodcastFetcher(BaseFetcher):
    """Apple Podcast 中文播客数据获取"""

    name = "apple_podcast"
    name_zh = "中文播客"
    icon = "🎧"
    color = "#9933FF"

    # 中文 AI/科技播客 RSS 源
    PODCASTS = {
        # 原有播客
        "https://harddecisions.fireside.fm/rss": "硬地骇客",
        "https://etw.fm/feed": "声东击西",
        "https://crazy.capital/feed": "疯投圈",
        "https://dao.fm/feed/": "津津乐道",
        "https://feeds.fireside.fm/zheshangye/rss": "商业就是这样",
        # 新增播客
        "https://feed.xyzfm.space/evgg6xle9rdc": "42章经",
        "https://feed.xyzfm.space/yxuruh3f9mc4": "乱翻书",
        "https://feeds.fireside.fm/guiguzaozhidao/rss": "硅谷早知道/科技早知道",
        "https://www.ximalaya.com/album/75918257.xml": "科技沉思录",
        "https://feed.xyzfm.space/dk4yh3pkpjp3": "张小珺｜商业访谈录",
        "https://feeds.fireside.fm/sv101/rss": "硅谷101",
        "https://feed.xyzfm.space/xxg7ryklkkft": "OnBoard!",
        "https://www.ximalaya.com/album/74194808.xml": "AI炼金术",
    }

    AI_KEYWORDS = [
        "AI", "人工智能", "GPT", "ChatGPT", "大模型", "LLM",
        "机器学习", "深度学习", "OpenAI", "Anthropic", "Claude",
        "AGI", "AIGC", "生成式", "智能", "Agent", "智能体",
        "Sora", "Midjourney", "科技", "技术", "创业", "硅谷",
    ]

    def fetch(self) -> list[FetchedItem]:
        items = []
        cutoff_time = datetime.now() - timedelta(hours=168)  # 7天内

        for rss_url, podcast_name in self.PODCASTS.items():
            try:
                episodes = self._fetch_podcast(rss_url, podcast_name, cutoff_time)
                items.extend(episodes)
                print(f"[ApplePodcast] Fetched {len(episodes)} from {podcast_name}")
            except Exception as e:
                print(f"[ApplePodcast] Error fetching {podcast_name}: {e}")

        items.sort(key=lambda x: x.pub_date or "", reverse=True)

        for idx, item in enumerate(items):
            base_score = max(100 - idx * 5, 10)
            ai_relevance = self._calculate_ai_relevance(item.title)
            item.fame_score = base_score + ai_relevance

        items.sort(key=lambda x: x.fame_score, reverse=True)
        return items[:15]

    def _fetch_podcast(self, rss_url: str, podcast_name: str, cutoff_time: datetime) -> list[FetchedItem]:
        feed = feedparser.parse(rss_url)
        items = []

        for entry in feed.entries[:10]:
            try:
                pub_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])

                if pub_date and pub_date < cutoff_time:
                    continue

                audio_url = ""
                if hasattr(entry, "enclosures") and entry.enclosures:
                    for enc in entry.enclosures:
                        if "audio" in enc.get("type", ""):
                            audio_url = enc.get("href", "")
                            break

                episode_id = hashlib.md5(entry.get("link", entry.get("id", "")).encode()).hexdigest()[:12]

                thumbnail = ""
                if hasattr(entry, "image") and entry.image:
                    thumbnail = entry.image.get("href", "")
                elif hasattr(feed.feed, "image") and feed.feed.image:
                    thumbnail = feed.feed.image.get("href", "")

                duration = entry.get("itunes_duration", "N/A")

                item = FetchedItem(
                    id=episode_id,
                    title=entry.get("title", ""),
                    link=entry.get("link", ""),
                    source=podcast_name,
                    author=podcast_name,
                    pub_date=pub_date.isoformat() if pub_date else "",
                    thumbnail=thumbnail,
                    summary=self._clean_summary(entry.get("summary", "")),
                    extra={
                        "audio_url": audio_url,
                        "duration": duration,
                        "podcast_name": podcast_name,
                    }
                )
                items.append(item)

            except Exception as e:
                print(f"[ApplePodcast] Error parsing entry: {e}")

        return items

    def _clean_summary(self, summary: str) -> str:
        clean = re.sub(r'<[^>]+>', '', summary)
        clean = clean.strip()[:500]
        return clean

    def _calculate_ai_relevance(self, title: str) -> int:
        score = 0
        for keyword in self.AI_KEYWORDS:
            if keyword.lower() in title.lower():
                score += 15
        return min(score, 60)
