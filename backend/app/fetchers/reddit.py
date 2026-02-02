import requests
from datetime import datetime, timedelta
from .base import BaseFetcher, FetchedItem


class RedditFetcher(BaseFetcher):
    """Reddit AI 相关话题数据获取"""

    name = "reddit"
    name_zh = "Reddit"
    icon = "🔴"
    color = "#ff4500"

    # AI 相关的 subreddit
    SUBREDDITS = [
        "MachineLearning",
        "artificial",
        "OpenAI",
        "LocalLLaMA",
        "ChatGPT",
        "ClaudeAI",
        "singularity",
        "StableDiffusion",
    ]

    def __init__(self):
        super().__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

    def fetch(self) -> list[FetchedItem]:
        self.items = []

        for subreddit in self.SUBREDDITS:
            print(f"  获取: r/{subreddit}...")
            posts = self._fetch_subreddit(subreddit)
            self.items.extend(posts)

        # 按分数排序
        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items[:30]

    def _fetch_subreddit(self, subreddit: str) -> list[FetchedItem]:
        """获取单个 subreddit 的热门帖子"""
        items = []
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=20"

        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
            if resp.status_code != 200:
                print(f"    获取失败: HTTP {resp.status_code}")
                return []

            data = resp.json()
            posts = data.get("data", {}).get("children", [])

            for post in posts:
                post_data = post.get("data", {})

                # 跳过置顶帖和广告
                if post_data.get("stickied") or post_data.get("is_video"):
                    continue

                # 检查时间（7天内）
                created_utc = post_data.get("created_utc", 0)
                post_time = datetime.fromtimestamp(created_utc)
                if datetime.now() - post_time > timedelta(days=7):
                    continue

                title = post_data.get("title", "")
                selftext = post_data.get("selftext", "")[:500]
                score = post_data.get("score", 0)
                num_comments = post_data.get("num_comments", 0)
                permalink = post_data.get("permalink", "")
                author = post_data.get("author", "")
                thumbnail = post_data.get("thumbnail", "")

                # 过滤无效缩略图
                if thumbnail in ["self", "default", "nsfw", "spoiler", ""]:
                    thumbnail = ""

                item = FetchedItem(
                    id=post_data.get("id", ""),
                    title=title,
                    link=f"https://www.reddit.com{permalink}",
                    source=f"r/{subreddit}",
                    author=f"u/{author}",
                    pub_date=post_time.isoformat(),
                    summary=selftext[:200] if selftext else "",
                    thumbnail=thumbnail,
                    extra={
                        "subreddit": subreddit,
                        "score": score,
                        "num_comments": num_comments,
                        "upvote_ratio": post_data.get("upvote_ratio", 0),
                        "flair": post_data.get("link_flair_text", ""),
                    }
                )

                item.tags = self._extract_tags(title, selftext, subreddit)
                item.fame_score = self._calculate_score(score, num_comments, subreddit)

                items.append(item)
                print(f"    + {title[:40]}... ({score} upvotes)")

        except Exception as e:
            print(f"    获取失败: {e}")

        return items

    def _extract_tags(self, title: str, text: str, subreddit: str) -> list:
        """提取标签"""
        tags = []
        combined = (title + " " + text).lower()
        seen = set()

        # Subreddit 作为标签
        subreddit_tags = {
            "MachineLearning": ("ML", "topic"),
            "OpenAI": ("OpenAI", "company"),
            "LocalLLaMA": ("LocalLLM", "topic"),
            "ChatGPT": ("ChatGPT", "topic"),
            "ClaudeAI": ("Claude", "company"),
            "StableDiffusion": ("SD", "topic"),
        }
        if subreddit in subreddit_tags:
            label, tag_type = subreddit_tags[subreddit]
            tags.append({"label": label, "type": tag_type})
            seen.add(label)

        # 关键词标签
        tag_patterns = [
            ("gpt-4|gpt-5|gpt4|gpt5", "GPT", "topic"),
            ("llama|mistral|qwen", "OpenSource", "topic"),
            ("fine-?tun", "FineTune", "topic"),
            ("rag|retrieval", "RAG", "topic"),
            ("agent", "Agent", "topic"),
            ("benchmark|eval", "Benchmark", "topic"),
        ]

        import re
        for pattern, label, tag_type in tag_patterns:
            if re.search(pattern, combined) and label not in seen:
                tags.append({"label": label, "type": tag_type})
                seen.add(label)
                if len(tags) >= 4:
                    break

        return tags

    def _calculate_score(self, upvotes: int, comments: int, subreddit: str) -> int:
        """计算热度分数"""
        score = 0

        # 基础分数（upvotes）
        if upvotes >= 1000:
            score += 50
        elif upvotes >= 500:
            score += 40
        elif upvotes >= 200:
            score += 30
        elif upvotes >= 100:
            score += 20
        elif upvotes >= 50:
            score += 10

        # 评论数加分
        if comments >= 200:
            score += 30
        elif comments >= 100:
            score += 20
        elif comments >= 50:
            score += 10

        # 热门 subreddit 加分
        hot_subreddits = ["MachineLearning", "LocalLLaMA", "OpenAI"]
        if subreddit in hot_subreddits:
            score += 15

        return score
