import feedparser
import re
from .base import BaseFetcher, FetchedItem


class SubstackFetcher(BaseFetcher):
    """Substack 文章数据获取"""

    name = "substack"
    name_zh = "Substack"
    icon = "📝"
    color = "#ff6719"

    # Substack 作者配置
    FEEDS = {
        "thebatch": {"name": "The Batch", "author": "Andrew Ng"},
        "importai": {"name": "Import AI", "author": "Jack Clark"},
        "oneusefulthing": {"name": "One Useful Thing", "author": "Ethan Mollick"},
        "interconnects": {"name": "Interconnects", "author": "Nathan Lambert"},
        "sebastianraschka": {"name": "Ahead of AI", "author": "Sebastian Raschka"},
        "chinatalk": {"name": "ChinaTalk", "author": "Jordan Schneider"},
        "aisnakeoil": {"name": "AI Snake Oil", "author": "Arvind Narayanan"},
    }

    # 关键词权重
    KEYWORD_WEIGHTS = {
        "gpt": 40, "openai": 50, "anthropic": 45, "claude": 45,
        "google": 40, "gemini": 40, "llama": 35, "meta": 30,
        "agent": 30, "reasoning": 35, "scaling": 30,
        "breakthrough": 40, "sota": 35, "benchmark": 25,
    }

    def fetch(self) -> list[FetchedItem]:
        """获取所有 Substack 文章"""
        self.items = []

        for slug, info in self.FEEDS.items():
            print(f"  获取: {info['name']} ({info['author']})")
            entries = self._fetch_rss(slug)

            for entry in entries:
                pub_date = entry.get("published", "")
                if not self.is_within_hours(pub_date, 48):  # 48小时内
                    continue

                item = FetchedItem(
                    id=entry.get("id", entry.get("link", "")),
                    title=entry.get("title", ""),
                    link=entry.get("link", ""),
                    source=info["name"],
                    author=info["author"],
                    pub_date=pub_date,
                    summary=self._clean_summary(entry.get("summary", "")),
                    extra={
                        "slug": slug,
                    }
                )

                item.tags = self._extract_tags(item.title, item.summary)
                item.fame_score = self._calculate_score(item)

                self.items.append(item)
                print(f"    + {item.title[:40]}...")

        # 按分数排序
        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_rss(self, slug: str) -> list:
        """获取 Substack RSS"""
        url = f"https://{slug}.substack.com/feed"
        try:
            feed = feedparser.parse(url)
            return feed.entries
        except Exception as e:
            print(f"    RSS 获取失败: {e}")
            return []

    @staticmethod
    def _clean_summary(html: str) -> str:
        """清理 HTML 摘要"""
        # 移除 HTML 标签
        text = re.sub(r'<[^>]+>', '', html)
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        # 截断
        if len(text) > 200:
            text = text[:200] + "..."
        return text

    def _extract_tags(self, title: str, summary: str) -> list:
        """提取标签"""
        tags = []
        text = (title + " " + summary).lower()
        seen = set()

        tag_patterns = [
            (r"openai|gpt-?[45o]", "OpenAI", "company"),
            (r"anthropic|claude", "Anthropic", "company"),
            (r"google|gemini|deepmind", "Google", "company"),
            (r"meta|llama", "Meta", "company"),
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
        """计算文章分数"""
        score = 0
        text = (item.title + " " + item.summary).lower()

        for keyword, weight in self.KEYWORD_WEIGHTS.items():
            if keyword in text:
                score += weight

        # 知名作者加分
        author_bonus = {
            "Andrew Ng": 30,
            "Ethan Mollick": 25,
            "Sebastian Raschka": 20,
        }
        score += author_bonus.get(item.author, 10)

        return score
