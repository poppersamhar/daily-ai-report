"""
Daily AI Report - 主入口
协调所有模块获取、处理和渲染
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from config import ENABLED_MODULES, MAX_ITEMS, OUTPUT_DIR
from fetchers import (
    YouTubeFetcher, SubstackFetcher, TwitterFetcher,
    ProductsFetcher, BusinessFetcher
)
from processors import Summarizer
from renderers import (
    IndexPageRenderer, YouTubePageRenderer, SubstackPageRenderer,
    TwitterPageRenderer, ProductsPageRenderer,
    BusinessPageRenderer
)


# 模块映射
FETCHER_MAP = {
    "youtube": YouTubeFetcher,
    "substack": SubstackFetcher,
    "twitter": TwitterFetcher,
    "products": ProductsFetcher,
    "business": BusinessFetcher,
}

RENDERER_MAP = {
    "youtube": YouTubePageRenderer,
    "substack": SubstackPageRenderer,
    "twitter": TwitterPageRenderer,
    "products": ProductsPageRenderer,
    "business": BusinessPageRenderer,
}

MODULE_TYPE_MAP = {
    "youtube": "video",
    "substack": "article",
    "twitter": "news",
    "products": "product",
    "business": "news",
}


def fetch_module(module_name: str) -> dict:
    """获取单个模块的数据"""
    print(f"\n[{module_name.upper()}] 开始获取...")

    fetcher_class = FETCHER_MAP.get(module_name)
    if not fetcher_class:
        print(f"  未知模块: {module_name}")
        return {"hero": None, "items": []}

    try:
        fetcher = fetcher_class()
        items = fetcher.fetch()
        hero = fetcher.get_hero()

        print(f"  获取到 {len(items)} 条内容")

        return {
            "hero": hero,
            "items": items[:MAX_ITEMS.get(module_name, 10)],
            "fetcher": fetcher,
        }
    except Exception as e:
        print(f"  获取失败: {e}")
        return {"hero": None, "items": []}


def process_module(module_name: str, data: dict, summarizer: Summarizer) -> dict:
    """处理单个模块的数据（AI 翻译/摘要）"""
    print(f"\n[{module_name.upper()}] 处理内容...")

    hero = data.get("hero")
    items = data.get("items", [])

    # 处理头条
    if hero:
        print(f"  处理头条: {hero.title[:40]}...")
        module_type = MODULE_TYPE_MAP.get(module_name, "article")
        hero = summarizer.process_hero(hero, module_type)

    # 批量翻译其他内容
    other_items = [item for item in items if item.id != (hero.id if hero else None)]
    if other_items:
        print(f"  翻译 {len(other_items[:5])} 条内容...")
        summarizer.batch_translate(other_items, limit=5)

    return {
        "hero": hero,
        "items": items,
    }


def render_module(module_name: str, data: dict, output_dir: Path) -> None:
    """渲染单个模块的页面"""
    print(f"\n[{module_name.upper()}] 生成页面...")

    renderer_class = RENDERER_MAP.get(module_name)
    if not renderer_class:
        return

    renderer = renderer_class()
    html = renderer.render(data.get("hero"), data.get("items", []))

    output_path = output_dir / f"{module_name}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"  已生成: {output_path}")


def render_index(modules_data: dict, output_dir: Path) -> None:
    """渲染首页"""
    print("\n[INDEX] 生成首页...")

    renderer = IndexPageRenderer()
    html = renderer.render(modules_data)

    output_path = output_dir / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"  已生成: {output_path}")


def main():
    print("=" * 60)
    print("Daily AI Report - 开始运行")
    print("=" * 60)

    # 创建输出目录
    output_dir = Path(__file__).parent / OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)

    # 初始化 AI 处理器
    summarizer = Summarizer()

    # 存储所有模块数据
    all_modules_data = {}

    # 1. 获取所有模块数据
    print("\n" + "=" * 40)
    print("阶段 1: 获取数据")
    print("=" * 40)

    for module_name in ENABLED_MODULES:
        data = fetch_module(module_name)
        all_modules_data[module_name] = data

    # 2. AI 处理（翻译/摘要）
    print("\n" + "=" * 40)
    print("阶段 2: AI 处理")
    print("=" * 40)

    for module_name in ENABLED_MODULES:
        data = all_modules_data.get(module_name, {})
        if data.get("hero") or data.get("items"):
            processed = process_module(module_name, data, summarizer)
            all_modules_data[module_name] = processed

    # 3. 渲染页面
    print("\n" + "=" * 40)
    print("阶段 3: 生成页面")
    print("=" * 40)

    # 渲染各模块详情页
    for module_name in ENABLED_MODULES:
        data = all_modules_data.get(module_name, {})
        render_module(module_name, data, output_dir)

    # 渲染首页
    render_index(all_modules_data, output_dir)

    # 4. 完成
    print("\n" + "=" * 60)
    print("完成！")
    print(f"输出目录: {output_dir}")
    print("=" * 60)

    # 统计
    total_items = sum(
        len(data.get("items", []))
        for data in all_modules_data.values()
    )
    print(f"\n总计获取 {total_items} 条内容")


if __name__ == "__main__":
    main()
