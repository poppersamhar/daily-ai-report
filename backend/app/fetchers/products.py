import requests
import re
from bs4 import BeautifulSoup
from .base import BaseFetcher, FetchedItem


class ProductsFetcher(BaseFetcher):
    """GitHub Trending 开源项目数据获取"""

    name = "products"
    name_zh = "开源项目"
    icon = "🚀"
    color = "#24292e"

    AI_KEYWORDS = [
        "ai", "ml", "llm", "gpt", "chatgpt", "claude", "gemini",
        "machine learning", "deep learning", "neural", "transformer",
        "langchain", "vector", "embedding", "rag", "agent",
        "openai", "anthropic", "huggingface", "pytorch", "tensorflow",
        "mcp", "model context protocol", "cursor", "copilot",
    ]

    def __init__(self):
        super().__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def fetch(self) -> list[FetchedItem]:
        self.items = []

        # 获取本周 GitHub Trending
        print("  获取 GitHub Trending (本周)...")
        gh_items = self._fetch_github_trending()

        # 对每个项目获取详细信息
        for item in gh_items[:20]:  # 限制数量避免请求过多
            print(f"    解析项目: {item.title[:30]}...")
            self._enrich_with_readme(item)
            self.items.append(item)

        self.items.sort(key=lambda x: x.fame_score, reverse=True)
        return self.items

    def _fetch_github_trending(self) -> list[FetchedItem]:
        """获取 GitHub Trending 项目（本周）"""
        items = []

        try:
            # 获取本周趋势
            url = "https://github.com/trending?since=weekly"
            resp = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(resp.text, "html.parser")

            articles = soup.select("article.Box-row")

            for article in articles[:30]:
                h2 = article.select_one("h2 a")
                if not h2:
                    continue

                repo_path = h2.get("href", "").strip("/")
                if not repo_path:
                    continue

                # 获取描述
                desc_elem = article.select_one("p")
                description = desc_elem.get_text(strip=True) if desc_elem else ""

                # AI 相关过滤
                if not self._is_ai_related(repo_path + " " + description):
                    continue

                # 获取编程语言
                lang_elem = article.select_one("[itemprop='programmingLanguage']")
                language = lang_elem.get_text(strip=True) if lang_elem else ""

                # 获取星标数
                stars_elem = article.select_one("a[href$='/stargazers']")
                stars_text = stars_elem.get_text(strip=True) if stars_elem else "0"
                stars = self._parse_stars(stars_text)

                # 获取本周新增星标
                stars_today_elem = article.select_one("span.d-inline-block.float-sm-right")
                stars_week = ""
                if stars_today_elem:
                    stars_week = stars_today_elem.get_text(strip=True)

                # 获取 forks
                forks_elem = article.select_one("a[href$='/forks']")
                forks = forks_elem.get_text(strip=True) if forks_elem else ""

                owner, repo_name = repo_path.split("/", 1) if "/" in repo_path else ("", repo_path)

                item = FetchedItem(
                    id=repo_path,
                    title=repo_name,
                    link=f"https://github.com/{repo_path}",
                    source="GitHub",
                    author=owner,
                    summary=description[:200] if description else "",
                    extra={
                        "type": "repo",
                        "repo_path": repo_path,
                        "owner": owner,
                        "language": language,
                        "stars": stars,
                        "stars_week": stars_week,
                        "forks": forks,
                    }
                )

                item.tags = self._extract_tags(repo_path + " " + description + " " + language)
                item.fame_score = self._calculate_score(item, stars)

                items.append(item)
                print(f"    + {repo_name[:40]}... ({stars} stars)")

        except Exception as e:
            print(f"    GitHub Trending 获取失败: {e}")

        return items

    def _enrich_with_readme(self, item: FetchedItem):
        """读取 README 获取项目详细信息"""
        repo_path = item.extra.get("repo_path", "")
        if not repo_path:
            return

        try:
            # 尝试获取 README
            readme_url = f"https://raw.githubusercontent.com/{repo_path}/main/README.md"
            resp = requests.get(readme_url, headers=self.headers, timeout=10)

            if resp.status_code == 404:
                # 尝试 master 分支
                readme_url = f"https://raw.githubusercontent.com/{repo_path}/master/README.md"
                resp = requests.get(readme_url, headers=self.headers, timeout=10)

            if resp.status_code == 200:
                readme_content = resp.text[:8000]  # 限制长度

                # 提取项目信息
                project_info = self._parse_readme(readme_content, item.title)

                # 更新 item
                if project_info.get("description"):
                    item.summary = project_info["description"][:300]

                item.extra.update({
                    "features": project_info.get("features", []),
                    "tech_stack": project_info.get("tech_stack", []),
                    "use_cases": project_info.get("use_cases", []),
                    "installation": project_info.get("installation", ""),
                })

        except Exception as e:
            print(f"      README 获取失败: {e}")

    def _parse_readme(self, content: str, repo_name: str) -> dict:
        """解析 README 内容提取关键信息"""
        result = {
            "description": "",
            "features": [],
            "tech_stack": [],
            "use_cases": [],
            "installation": "",
        }

        lines = content.split("\n")
        current_section = None

        for line in lines:
            line_lower = line.lower().strip()

            # 检测章节标题
            if line.startswith("#"):
                if any(kw in line_lower for kw in ["feature", "功能", "特性", "what"]):
                    current_section = "features"
                elif any(kw in line_lower for kw in ["install", "安装", "getting started", "quick start", "usage"]):
                    current_section = "installation"
                elif any(kw in line_lower for kw in ["tech", "stack", "built with", "依赖", "技术"]):
                    current_section = "tech_stack"
                elif any(kw in line_lower for kw in ["use case", "用例", "example", "demo"]):
                    current_section = "use_cases"
                else:
                    current_section = None
                continue

            # 提取描述（第一段非空文本）
            if not result["description"] and line.strip() and not line.startswith(("#", "!", "[", "<", "|", "-", "*", "`")):
                # 跳过徽章行
                if "badge" not in line_lower and "shield" not in line_lower and "img.shields" not in line:
                    result["description"] = self._clean_markdown(line.strip())

            # 提取列表项
            if current_section and (line.strip().startswith("-") or line.strip().startswith("*") or re.match(r"^\d+\.", line.strip())):
                item_text = re.sub(r"^[-*\d.]+\s*", "", line.strip())
                item_text = self._clean_markdown(item_text)
                if item_text and len(item_text) > 5:
                    if current_section == "features" and len(result["features"]) < 5:
                        result["features"].append(item_text[:100])
                    elif current_section == "tech_stack" and len(result["tech_stack"]) < 5:
                        result["tech_stack"].append(item_text[:50])
                    elif current_section == "use_cases" and len(result["use_cases"]) < 3:
                        result["use_cases"].append(item_text[:100])

            # 提取安装命令
            if current_section == "installation" and line.strip().startswith(("pip ", "npm ", "yarn ", "cargo ", "go ")):
                result["installation"] = line.strip()[:100]

        # 从内容中提取技术栈关键词
        if not result["tech_stack"]:
            tech_keywords = ["python", "typescript", "javascript", "rust", "go", "react", "vue", "nextjs",
                           "fastapi", "flask", "django", "pytorch", "tensorflow", "langchain", "llamaindex"]
            content_lower = content.lower()
            for tech in tech_keywords:
                if tech in content_lower:
                    result["tech_stack"].append(tech.capitalize())
                if len(result["tech_stack"]) >= 5:
                    break

        return result

    def _clean_markdown(self, text: str) -> str:
        """清理 Markdown 格式"""
        # 移除链接
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # 移除图片
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
        # 移除加粗/斜体
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        # 移除代码块标记
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # 清理多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _parse_stars(self, stars_text: str) -> int:
        """解析星标数"""
        stars_text = stars_text.strip().lower().replace(",", "")
        try:
            if "k" in stars_text:
                return int(float(stars_text.replace("k", "")) * 1000)
            return int(stars_text)
        except:
            return 0

    def _is_ai_related(self, text: str) -> bool:
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.AI_KEYWORDS)

    def _extract_tags(self, text: str) -> list:
        tags = []
        text_lower = text.lower()
        seen = set()

        tag_patterns = [
            (r"llm|gpt|claude|gemini", "LLM", "tech"),
            (r"agent", "Agent", "tech"),
            (r"rag|vector|embedding", "RAG", "tech"),
            (r"langchain|llamaindex", "Framework", "tech"),
            (r"mcp|model context", "MCP", "tech"),
            (r"python", "Python", "lang"),
            (r"typescript|javascript", "TypeScript", "lang"),
            (r"rust", "Rust", "lang"),
            (r"go\b|golang", "Go", "lang"),
        ]

        for pattern, label, tag_type in tag_patterns:
            if re.search(pattern, text_lower) and label not in seen:
                tags.append({"label": label, "type": tag_type})
                seen.add(label)

        return tags[:4]

    def _calculate_score(self, item: FetchedItem, stars: int) -> int:
        score = 0
        text_lower = (item.title + " " + item.summary).lower()

        # 关键词权重
        keyword_weights = {
            "llm": 40, "gpt": 35, "claude": 35, "agent": 35,
            "rag": 30, "langchain": 30, "openai": 40,
            "anthropic": 40, "huggingface": 30, "mcp": 35,
        }

        for keyword, weight in keyword_weights.items():
            if keyword in text_lower:
                score += weight

        # 星标数加分
        if stars >= 10000:
            score += 50
        elif stars >= 5000:
            score += 40
        elif stars >= 1000:
            score += 30
        elif stars >= 500:
            score += 20
        elif stars >= 100:
            score += 10

        return score
