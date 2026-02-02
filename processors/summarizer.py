from .deepseek import get_client, DeepSeekClient
from fetchers.base import FetchedItem


class Summarizer:
    """通用摘要/翻译处理器"""

    def __init__(self, client: DeepSeekClient = None):
        self.client = client or get_client()

    def translate_title(self, item: FetchedItem) -> FetchedItem:
        """翻译标题"""
        prompt = f"""将以下标题翻译成简洁的中文：

原标题：{item.title}

只输出翻译后的中文标题，不要任何解释。"""

        result = self.client.call(prompt)
        if result:
            item.title_zh = result.strip()
        else:
            item.title_zh = item.title

        return item

    def translate_and_summarize(self, item: FetchedItem) -> FetchedItem:
        """翻译标题并生成摘要"""
        prompt = f"""将以下内容翻译成中文，并生成简短摘要。

原标题：{item.title}
来源：{item.source}
原摘要：{item.summary[:200] if item.summary else '无'}

输出 JSON 格式：
{{"title_zh": "中文标题", "summary": "一句话摘要（20-30字）"}}

只输出 JSON，不要其他内容。"""

        data = self.client.call_json(prompt)
        if data:
            item.title_zh = data.get("title_zh", item.title)
            if not item.summary:
                item.summary = data.get("summary", "")

        return item

    def process_hero(self, item: FetchedItem, module_type: str = "video") -> FetchedItem:
        """处理头条内容 - 生成深度总结"""
        type_hints = {
            "video": "视频",
            "article": "文章",
            "paper": "论文",
            "product": "产品",
            "news": "新闻",
        }
        type_name = type_hints.get(module_type, "内容")

        prompt = f"""你是一名资深 AI 研究员。根据以下{type_name}信息生成深度总结。

标题：{item.title}
来源：{item.source}
摘要：{item.summary[:300] if item.summary else '无'}

输出 JSON 格式：
{{
  "title_zh": "中文标题（简洁有力）",
  "summary": "60-80字中文摘要",
  "core_insight": "一句话核心认知",
  "key_points": ["要点1", "要点2", "要点3"]
}}

只输出 JSON，不要其他内容。"""

        data = self.client.call_json(prompt)
        if data:
            item.title_zh = data.get("title_zh", item.title)
            item.summary = data.get("summary", item.summary)
            item.extra["core_insight"] = data.get("core_insight", "")
            item.extra["key_points"] = data.get("key_points", [])

        return item

    def select_hero(self, items: list[FetchedItem], module_name: str = "") -> FetchedItem:
        """AI 筛选头条"""
        if not items:
            return None

        if len(items) == 1:
            return items[0]

        # 构建列表
        item_list = "\n".join([
            f"{i+1}. [{item.source}] {item.title}"
            for i, item in enumerate(items[:10])
        ])

        prompt = f"""你是一位严格的 AI 科技主编。从下方{module_name}列表中选出 1 个最具价值的内容作为今日头条。

筛选标准（优先级从高到低）：
1. 涉及 OpenAI/Google/Anthropic/NVIDIA 等巨头的重大发布
2. 涉及 Sam Altman/Andrej Karpathy/Dario Amodei 等顶流人物
3. 涉及具体技术突破或重要研究成果
4. 时效性和影响力

内容列表：
{item_list}

只返回被选中内容的序号（如 1），不要任何解释。"""

        result = self.client.call(prompt)

        try:
            import re
            idx = int(re.search(r'\d+', result).group()) - 1
            if 0 <= idx < len(items):
                return items[idx]
        except:
            pass

        # 默认返回第一个
        return items[0]

    def batch_translate(self, items: list[FetchedItem], limit: int = 10) -> list[FetchedItem]:
        """批量翻译标题"""
        for item in items[:limit]:
            if not item.title_zh:
                self.translate_title(item)
        return items
