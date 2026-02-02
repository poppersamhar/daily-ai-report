import feedparser
import re
import requests
from bs4 import BeautifulSoup
from .base import BaseFetcher, FetchedItem


class SubstackFetcher(BaseFetcher):
    """Substack 及 AI 公司官方博客数据获取"""

    name = "substack"
    name_zh = "Substack"
    icon = "📝"
    color = "#ff6719"

    # Substack RSS 源
    SUBSTACK_FEEDS = {
        "thebatch": {"name": "The Batch", "author": "Andrew Ng"},
        "importai": {"name": "Import AI", "author": "Jack Clark"},
        "oneusefulthing": {"name": "One Useful Thing", "author": "Ethan Mollick"},
        "interconnects": {"name": "Interconnects", "author": "Nathan Lambert"},
        "sebastianraschka": {"name": "Ahead of AI", "author": "Sebastian Raschka"},
        "chinatalk": {"name": "ChinaTalk", "author": "Jordan Schneider"},
        "aisnakeoil": {"name": "AI Snake Oil", "author": "Arvind Narayanan"},
        "bensbites": {"name": "Ben's Bites", "author": "Ben Tossell"},
        "creatoreconomy": {"name": "Creator Economy", "author": "Peter Yang"},
    }

    # 官方博客 RSS 源
    OFFICIAL_FEEDS = {
        "https://openai.com/blog/rss.xml": {"name": "OpenAI Blog", "author": "OpenAI"},
        "https://www.anthropic.com/rss.xml": {"name": "Anthropic News", "author": "Anthropic"},
        "https://blog.google/technology/ai/rss/": {"name": "Google AI Blog", "author": "Google"},
        "https://ai.meta.com/blog/rss/": {"name": "Meta AI Blog", "author": "Meta"},
        "https://x.ai/blog/rss.xml": {"name": "xAI News", "author": "xAI"},
        "https://mistral.ai/feed.xml": {"name": "Mistral AI News", "author": "Mistral"},
    }

    KEYWORD_WEIGHTS = {
        "gpt": 40, "openai": 50, "anthropic": 45, "claude": 45,
        "google": 40, "gemini": 40, "llama": 35, "meta": 30,
        "agent": 30, "reasoning": 35, "scaling": 30,
        "breakthrough": 40, "sota": 35, "benchmark": 25,
        "grok": 35, "mistral": 35,
    }

    def fetch(self) -> list[FetchedItem]:
        self.items = []

        # 1. 获取 Substack 源
        for slug, info in self.SUBSTACK_FEEDS.items():
            print(f"  获取: {info['name']} ({info['author']})")
            entries = self._fetch_substack_rss(slug)

            for entry in entries:
                pub_date = entry.get("published", "")
                if not self.is_within_hours(pub_date, 168):
                    continue

                item = FetchedItem(
                    id=entry.get("id", entry.get("link", "")),
                    title=entry.get("title", ""),
                    link=entry.get("link", ""),
                    source=info["name"],
                    author=info["author"],
                    pub_date=pub_date,
                    summary=self._clean_summary(entry.get("summary", "")),
                    extra={"slug": slug, "type": "substack"}
                )

                item.tags = self._extract_tags(item.title, item.summary)
                item.fame_score = self._calculate_score(item)

                self.items.append(item)
                print(f"    + {item.title[:40]}...")

        # 2. 获取官方博客源
        for url, info in self.OFFICIAL_FEEDS.items():
            print(f"  获取: {info['name']}")
            entries = self._fetch_official_rss(url)

            for entry in entries:
                pub_date = entry.get("published", "") or entry.get("updated", "")
                if not self.is_within_hours(pub_date, 168):
                    continue

                item = FetchedItem(
                    id=entry.get("id", entry.get("link", "")),
                    title=entry.get("title", ""),
                    link=entry.get("link", ""),
                    source=info["name"],
                    author=info["author"],
                    pub_date=pub_date,
                    summary=self._clean_summary(entry.get("summary", "") or entry.get("description", "")),
                    extra={"url": url, "type": "official"}
                )

                item.tags = self._extract_tags(item.title, item.summary)
                item.fame_score = self._calculate_score(item)
                # 官方博客加分
                item.fame_score += 30

                self.items.append(item)
                print(f"    + {item.title[:40]}...")

        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_substack_rss(self, slug: str) -> list:
        url = f"https://{slug}.substack.com/feed"
        try:
            feed = feedparser.parse(url)
            return feed.entries
        except Exception as e:
            print(f"    RSS 获取失败: {e}")
            return []

    def _fetch_official_rss(self, url: str) -> list:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            }
            feed = feedparser.parse(url, request_headers=headers)
            return feed.entries[:10]
        except Exception as e:
            print(f"    RSS 获取失败: {e}")
            return []

    @staticmethod
    def _clean_summary(html: str) -> str:
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 200:
            text = text[:200] + "..."
        return text

    def _extract_tags(self, title: str, summary: str) -> list:
        tags = []
        text = (title + " " + summary).lower()
        seen = set()

        tag_patterns = [
            (r"openai|gpt-?[45o]", "OpenAI", "company"),
            (r"anthropic|claude", "Anthropic", "company"),
            (r"google|gemini|deepmind", "Google", "company"),
            (r"meta|llama", "Meta", "company"),
            (r"mistral", "Mistral", "company"),
            (r"xai|grok", "xAI", "company"),
            (r"agent", "Agent", "topic"),
            (r"reasoning", "Reasoning", "topic"),
            (r"scaling", "Scaling", "topic"),
        ]

        for pattern, label, tag_type in tag_patterns:
            if re.search(pattern, text) and label not in seen:
                tags.append({"label": label, "type": tag_type})
                seen.add(label)

        return tags[:4]

    def _calculate_score(self, item: FetchedItem) -> int:
        score = 0
        text = (item.title + " " + item.summary).lower()

        for keyword, weight in self.KEYWORD_WEIGHTS.items():
            if keyword in text:
                score += weight

        author_bonus = {
            "Andrew Ng": 30,
            "Ethan Mollick": 25,
            "Sebastian Raschka": 20,
            "OpenAI": 40,
            "Anthropic": 40,
            "Google": 35,
            "Meta": 30,
            "xAI": 30,
            "Mistral": 30,
        }
        score += author_bonus.get(item.author, 10)

        return score
