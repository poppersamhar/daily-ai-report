import feedparser
import re
from .base import BaseFetcher, FetchedItem


class BusinessFetcher(BaseFetcher):
    """AI 商业新闻数据获取"""

    name = "business"
    name_zh = "AI 商业"
    icon = "💼"
    color = "#2ecc71"

    RSS_FEEDS = {
        "techcrunch_ai": {
            "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "name": "TechCrunch AI",
        },
        "venturebeat_ai": {
            "url": "https://venturebeat.com/category/ai/feed/",
            "name": "VentureBeat AI",
        },
        "theverge_ai": {
            "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
            "name": "The Verge AI",
        },
        "wired_ai": {
            "url": "https://www.wired.com/feed/tag/ai/latest/rss",
            "name": "Wired AI",
        },
    }

    KEYWORD_WEIGHTS = {
        "funding": 50, "raised": 50, "series": 45, "investment": 45,
        "valuation": 50, "billion": 45, "million": 35,
        "acquisition": 50, "acquire": 50, "merger": 45,
        "ipo": 55, "public": 40, "stock": 35,
        "partnership": 40, "deal": 35, "contract": 35,
        "launch": 40, "release": 40, "announce": 35,
        "openai": 45, "anthropic": 45, "google": 40,
        "microsoft": 40, "nvidia": 45, "meta": 35,
    }

    def fetch(self) -> list[FetchedItem]:
        self.items = []

        for feed_id, feed_info in self.RSS_FEEDS.items():
            print(f"  获取: {feed_info['name']}...")
            entries = self._fetch_rss(feed_info["url"])

            for entry in entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")

                if not self._is_business_related(title + " " + summary):
                    continue

                pub_date = entry.get("published", "")
                if not self.is_within_hours(pub_date, 168):
                    continue

                item = FetchedItem(
                    id=entry.get("id", entry.get("link", "")),
                    title=title,
                    link=entry.get("link", ""),
                    source=feed_info["name"],
                    summary=self._clean_summary(summary),
                    pub_date=pub_date,
                    extra={"feed_id": feed_id}
                )

                item.tags = self._extract_tags(title + " " + summary)
                item.fame_score = self._calculate_score(item)

                self.items.append(item)
                print(f"    + {item.title[:40]}...")

        self.items = self._deduplicate(self.items)
        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_rss(self, url: str) -> list:
        try:
            feed = feedparser.parse(url)
            return feed.entries[:15]
        except Exception as e:
            print(f"    RSS 获取失败: {e}")
            return []

    def _is_business_related(self, text: str) -> bool:
        text_lower = text.lower()
        business_keywords = [
            "funding", "raised", "series", "investment", "valuation",
            "acquisition", "acquire", "merger", "ipo", "partnership",
            "deal", "billion", "million", "revenue", "profit",
        ]
        return any(kw in text_lower for kw in business_keywords)

    @staticmethod
    def _clean_summary(html: str) -> str:
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 200:
            text = text[:200] + "..."
        return text

    def _extract_tags(self, text: str) -> list:
        tags = []
        text_lower = text.lower()
        seen = set()

        tag_patterns = [
            (r"funding|raised|series|investment", "融资", "event"),
            (r"acquisition|acquire|merger", "收购", "event"),
            (r"ipo|public offering", "IPO", "event"),
            (r"partnership|deal", "合作", "event"),
            (r"openai", "OpenAI", "company"),
            (r"anthropic", "Anthropic", "company"),
            (r"nvidia", "NVIDIA", "company"),
            (r"google|deepmind", "Google", "company"),
            (r"microsoft", "Microsoft", "company"),
        ]

        for pattern, label, tag_type in tag_patterns:
            if re.search(pattern, text_lower) and label not in seen:
                tags.append({"label": label, "type": tag_type})
                seen.add(label)

        return tags[:4]

    def _calculate_score(self, item: FetchedItem) -> int:
        score = 0
        text_lower = (item.title + " " + item.summary).lower()

        for keyword, weight in self.KEYWORD_WEIGHTS.items():
            if keyword in text_lower:
                score += weight

        source_weights = {
            "TechCrunch AI": 20,
            "VentureBeat AI": 15,
            "The Verge AI": 10,
            "Wired AI": 10,
        }
        score += source_weights.get(item.source, 5)

        return score

    def _deduplicate(self, items: list[FetchedItem]) -> list[FetchedItem]:
        seen_titles = set()
        unique_items = []

        for item in items:
            simple_title = re.sub(r'[^a-z0-9]', '', item.title.lower())[:50]
            if simple_title not in seen_titles:
                seen_titles.add(simple_title)
                unique_items.append(item)

        return unique_items
