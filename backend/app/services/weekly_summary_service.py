import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.item import Item
from app.models.weekly_summary import WeeklySummary
from app.processors.deepseek import get_client


def generate_weekly_summary(db: Session) -> WeeklySummary:
    """Generate weekly summary from items in the database"""
    client = get_client()

    # Calculate week range
    now = datetime.now()
    week_end = now.date()
    week_start = (now - timedelta(days=7)).date()

    # Get all items from the past 7 days
    cutoff = now - timedelta(days=7)
    items = db.query(Item).filter(
        Item.pub_date >= cutoff
    ).order_by(desc(Item.fame_score)).all()

    if not items:
        return None

    # Collect module stats
    modules_stats = {}
    for item in items:
        module = item.module
        if module not in modules_stats:
            modules_stats[module] = {"count": 0, "top_items": []}
        modules_stats[module]["count"] += 1
        if len(modules_stats[module]["top_items"]) < 3:
            modules_stats[module]["top_items"].append(item.title_zh or item.title)

    # Prepare content for AI analysis
    top_items_text = "\n".join([
        f"- [{item.module}] {item.title_zh or item.title}"
        for item in items[:50]
    ])

    prompt = f"""你是一位资深 AI 行业分析师。请根据以下本周 AI 领域的重要内容，生成一份周报汇总。

本周内容（按重要性排序）：
{top_items_text}

请输出 JSON 格式：
{{
  "headline": "本周最重要的一条新闻标题（20字以内）",
  "hot_topics": [
    {{"topic": "热点话题1", "description": "简短描述（30字）", "trend": "上升/下降/持平"}},
    {{"topic": "热点话题2", "description": "简短描述（30字）", "trend": "上升/下降/持平"}},
    {{"topic": "热点话题3", "description": "简短描述（30字）", "trend": "上升/下降/持平"}}
  ],
  "trend_analysis": "本周 AI 行业整体趋势分析（100-150字）",
  "key_events": [
    {{"title": "重要事件1", "summary": "事件摘要（30字）"}},
    {{"title": "重要事件2", "summary": "事件摘要（30字）"}},
    {{"title": "重要事件3", "summary": "事件摘要（30字)"}}
  ],
  "company_mentions": {{"OpenAI": 5, "Anthropic": 3, "Google": 4}}
}}

注意：
- hot_topics 提取3-5个本周最热门的话题
- key_events 提取3-5个本周最重要的事件
- company_mentions 统计主要 AI 公司被提及的次数
- 所有内容用中文输出

只输出 JSON，不要其他内容。"""

    data = client.call_json(prompt)

    if not data:
        return None

    # Create weekly summary
    summary = WeeklySummary(
        id=str(uuid.uuid4()),
        week_start=week_start,
        week_end=week_end,
        headline=data.get("headline", ""),
        hot_topics=data.get("hot_topics", []),
        trend_analysis=data.get("trend_analysis", ""),
        key_events=data.get("key_events", []),
        company_mentions=data.get("company_mentions", {}),
        total_items=len(items),
        modules_stats=modules_stats,
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary


def get_latest_weekly_summary(db: Session) -> WeeklySummary:
    """Get the most recent weekly summary"""
    return db.query(WeeklySummary).order_by(
        desc(WeeklySummary.created_at)
    ).first()
