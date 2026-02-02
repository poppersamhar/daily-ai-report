import requests
import feedparser
import re
from bs4 import BeautifulSoup
from .base import BaseFetcher, FetchedItem


class ProductsFetcher(BaseFetcher):
    """ProductHunt + GitHub Trending 数据获取"""

    name = "products"
    name_zh = "产品/开源"
    icon = "🚀"
    color = "#da552f"

    # AI 相关关键词
    AI_KEYWORDS = [
        "ai", "ml", "llm", "gpt", "chatgpt", "claude", "gemini",
        "machine learning", "deep learning", "neural", "transformer",
        "langchain", "vector", "embedding", "rag", "agent",
        "openai", "anthropic", "huggingface", "pytorch", "tensorflow",
    ]

    def fetch(self) -> list[FetchedItem]:
        """获取产品和开源项目"""
        self.items = []

        # 获取 ProductHunt
        print("  获取 ProductHunt...")
        ph_items = self._fetch_producthunt()
        self.items.extend(ph_items)

        # 获取 GitHub Trending
        print("  获取 GitHub Trending...")
        gh_items = self._fetch_github_trending()
        self.items.extend(gh_items)

        # 按分数排序
        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_producthunt(self) -> list[FetchedItem]:
        """获取 ProductHunt 热门产品"""
        items = []

        # 使用 RSS feed
        try:
            feed = feedparser.parse("https://www.producthunt.com/feed")
            for entry in feed.entries[:20]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")

                # 过滤非 AI 相关
                if not self._is_ai_related(title + " " + summary):
                    continue

                pub_date = entry.get("published", "")
                if not self.is_within_hours(pub_date, 48):
                    continue

                item = FetchedItem(
                    id=entry.get("id", entry.get("link", "")),
                    title=title,
                    link=entry.get("link", ""),
                    source="ProductHunt",
                    summary=self._clean_html(summary)[:150],
                    pub_date=pub_date,
                    extra={"type": "product"}
                )

                item.tags = self._extract_tags(title + " " + summary)
                item.fame_score = self._calculate_score(item)

                items.append(item)
                print(f"    + [PH] {item.title[:40]}...")

        except Exception as e:
            print(f"    ProductHunt 获取失败: {e}")

        return items

    def _fetch_github_trending(self) -> list[FetchedItem]:
        """获取 GitHub Trending 项目"""
        items = []

        try:
            # 爬取 GitHub Trending 页面
            url = "https://github.com/trending?since=daily"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(resp.text, "html.parser")

            # 解析项目列表
            articles = soup.select("article.Box-row")

            for article in articles[:30]:
                # 获取项目名称和链接
                h2 = article.select_one("h2 a")
                if not h2:
                    continue

                repo_path = h2.get("href", "").strip("/")
                if not repo_path:
                    continue

                title = repo_path.replace("/", " / ")
                link = f"https://github.com/{repo_path}"

                # 获取描述
                desc_elem = article.select_one("p")
                description = desc_elem.get_text(strip=True) if desc_elem else ""

                # 过滤非 AI 相关
                if not self._is_ai_related(title + " " + description):
                    continue

                # 获取语言
                lang_elem = article.select_one("[itemprop='programmingLanguage']")
                language = lang_elem.get_text(strip=True) if lang_elem else ""

                # 获取星标数
                stars_elem = article.select_one("a[href$='/stargazers']")
                stars = stars_elem.get_text(strip=True) if stars_elem else ""

                item = FetchedItem(
                    id=repo_path,
                    title=title,
                    link=link,
                    source="GitHub",
                    summary=description[:150] if description else "",
                    extra={
                        "type": "repo",
                        "language": language,
                        "stars": stars,
                    }
                )

                item.tags = self._extract_tags(title + " " + description)
                item.fame_score = self._calculate_score(item)

                items.append(item)
                print(f"    + [GH] {item.title[:40]}...")

        except Exception as e:
            print(f"    GitHub Trending 获取失败: {e}")

        return items

    def _is_ai_related(self, text: str) -> bool:
        """判断是否 AI 相关"""
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.AI_KEYWORDS)

    @staticmethod
    def _clean_html(html: str) -> str:
        """清理 HTML"""
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_tags(self, text: str) -> list:
        """提取标签"""
        tags = []
        text_lower = text.lower()
        seen = set()

        tag_patterns = [
            (r"llm|gpt|claude|gemini", "LLM", "tech"),
            (r"agent", "Agent", "tech"),
            (r"rag|vector|embedding", "RAG", "tech"),
            (r"langchain|llamaindex", "Framework", "tech"),
            (r"python", "Python", "lang"),
            (r"typescript|javascript", "TypeScript", "lang"),
            (r"rust", "Rust", "lang"),
        ]

        for pattern, label, tag_type in tag_patterns:
            if re.search(pattern, text_lower) and label not in seen:
                tags.append({"label": label, "type": tag_type})
                seen.add(label)

        return tags[:4]

    def _calculate_score(self, item: FetchedItem) -> int:
        """计算分数"""
        score = 0
        text_lower = (item.title + " " + item.summary).lower()

        # 关键词权重
        keyword_weights = {
            "llm": 40, "gpt": 35, "claude": 35, "agent": 35,
            "rag": 30, "langchain": 30, "openai": 40,
            "anthropic": 40, "huggingface": 30,
        }

        for keyword, weight in keyword_weights.items():
            if keyword in text_lower:
                score += weight

        # 来源加分
        if item.source == "GitHub":
            score += 10
        elif item.source == "ProductHunt":
            score += 15

        return score
