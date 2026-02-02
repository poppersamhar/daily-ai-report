from fetchers.base import FetchedItem
from .base import wrap_html, render_header
from .components import (
    render_hero_card, render_item_card, render_compact_card,
    render_module_preview
)


class IndexPageRenderer:
    """首页渲染器"""

    def render(self, modules_data: dict) -> str:
        """渲染首页

        Args:
            modules_data: {
                "youtube": {"hero": FetchedItem, "items": [FetchedItem, ...]},
                "substack": {...},
                ...
            }
        """
        header = render_header("Daily AI Report", "AI 领域每日精选", "每日更新")

        # 渲染模块预览
        modules_html = '<div class="modules-grid">'

        module_configs = [
            ("youtube", "YouTube/播客", "🎬", "youtube.html"),
            ("substack", "Substack", "📝", "substack.html"),
            ("twitter", "X/Twitter", "🐦", "twitter.html"),
            ("products", "产品/开源", "🚀", "products.html"),
            ("business", "AI 商业", "💼", "business.html"),
        ]

        for module_name, module_name_zh, icon, detail_page in module_configs:
            data = modules_data.get(module_name, {})
            hero = data.get("hero")
            items = data.get("items", [])

            if hero or items:
                modules_html += render_module_preview(
                    module_name, module_name_zh, icon,
                    hero, items, detail_page
                )

        modules_html += '</div>'

        content = f'''
  {header}

  <div class="container">
    <div class="section-title">今日概览</div>
    {modules_html}
  </div>'''

        return wrap_html(content, "Daily AI Report - 每日 AI 精选", "index")


class DetailPageRenderer:
    """详情页渲染器基类"""

    module_name = "module"
    module_name_zh = "模块"
    icon = "📄"
    badge = "精选"

    def render(self, hero: FetchedItem, items: list[FetchedItem]) -> str:
        """渲染详情页"""
        header = render_header(self.module_name_zh, "精选内容", self.badge)

        hero_html = ""
        if hero:
            hero_html = f'''
    <div class="section-title">今日精选</div>
    {render_hero_card(hero, self.icon, "精选推荐")}'''

        items_html = ""
        if items:
            items_html = f'<div class="section-title">更多内容</div>'
            for item in items:
                if item.id != (hero.id if hero else None):
                    items_html += self.render_item(item)

        empty_html = ""
        if not hero and not items:
            empty_html = '''
    <div class="empty-state">
      <div class="icon">📭</div>
      <p>暂无最新内容</p>
    </div>'''

        content = f'''
  {header}

  <div class="container">
    {hero_html}
    {items_html}
    {empty_html}
  </div>'''

        return wrap_html(content, f"{self.module_name_zh} - Daily AI Report", self.module_name)

    def render_item(self, item: FetchedItem) -> str:
        """渲染单个内容项，子类可覆盖"""
        return render_item_card(item)


class YouTubePageRenderer(DetailPageRenderer):
    """YouTube 详情页渲染器"""
    module_name = "youtube"
    module_name_zh = "YouTube/播客"
    icon = "🎬"
    badge = "YouTube 精选"

    def render_item(self, item: FetchedItem) -> str:
        return render_item_card(item, show_thumbnail=True)


class SubstackPageRenderer(DetailPageRenderer):
    """Substack 详情页渲染器"""
    module_name = "substack"
    module_name_zh = "Substack"
    icon = "📝"
    badge = "Substack 精选"

    def render_item(self, item: FetchedItem) -> str:
        return render_compact_card(item)


class TwitterPageRenderer(DetailPageRenderer):
    """Twitter 详情页渲染器"""
    module_name = "twitter"
    module_name_zh = "X/Twitter"
    icon = "🐦"
    badge = "Twitter 动态"

    def render_item(self, item: FetchedItem) -> str:
        return render_compact_card(item)


class ProductsPageRenderer(DetailPageRenderer):
    """产品详情页渲染器"""
    module_name = "products"
    module_name_zh = "产品/开源"
    icon = "🚀"
    badge = "产品精选"

    def render_item(self, item: FetchedItem) -> str:
        return render_compact_card(item)


class BusinessPageRenderer(DetailPageRenderer):
    """商业详情页渲染器"""
    module_name = "business"
    module_name_zh = "AI 商业"
    icon = "💼"
    badge = "商业动态"

    def render_item(self, item: FetchedItem) -> str:
        return render_compact_card(item)
