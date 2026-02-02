from datetime import datetime
from fetchers.base import FetchedItem


def render_tags(tags: list) -> str:
    """渲染标签 HTML"""
    if not tags:
        return ""
    html_tags = []
    for tag in tags[:3]:
        tag_type = tag.get("type", "topic")
        cls = {
            "company": "company",
            "person": "person",
            "topic": "topic",
            "tech": "tech",
            "event": "event",
            "lang": "lang",
        }.get(tag_type, "topic")
        html_tags.append(f'<span class="tag {cls}">{tag["label"]}</span>')
    return "".join(html_tags)


def render_key_points(points: list) -> str:
    """渲染要点列表"""
    if not points:
        return ""
    return "".join([f"<li>{p}</li>" for p in points])


def time_ago(date_str: str) -> str:
    """计算时间差"""
    try:
        from dateutil import parser
        pub_date = parser.parse(date_str)
        now = datetime.now(pub_date.tzinfo)
        diff = now - pub_date
        hours = int(diff.total_seconds() / 3600)

        if hours < 1:
            return "刚刚"
        elif hours < 24:
            return f"{hours}小时前"
        else:
            return f"{hours // 24}天前"
    except:
        return ""


def render_hero_card(item: FetchedItem, module_icon: str = "🎬", module_name: str = "精选") -> str:
    """渲染头条卡片"""
    duration_html = ""
    if item.extra.get("duration"):
        duration_html = f'<span class="duration">{item.extra["duration"]}</span>'

    thumbnail_html = ""
    if item.thumbnail:
        thumbnail_html = f'''
      <div class="hero-thumb">
        <span class="hero-badge">{module_icon} {module_name}</span>
        <img src="{item.thumbnail}" alt="" onerror="this.style.display='none'">
        {duration_html}
      </div>'''

    core_insight = item.extra.get("core_insight", "")
    key_points = item.extra.get("key_points", [])

    expand_content = ""
    if core_insight or key_points:
        expand_content = f'''
      <button class="expand-btn" onclick="toggleExpand(this)">
        <span>查看详情</span>
        <span class="arrow">▼</span>
      </button>

      <div class="expand-content">
        <div class="expand-inner">
          <div class="insight-box">
            <div class="insight-label">核心观点</div>
            <div class="insight-text">{core_insight}</div>
            <ul class="key-points">
              {render_key_points(key_points)}
            </ul>
          </div>

          <a href="{item.link}" target="_blank" class="watch-btn">
            查看原文
          </a>
        </div>
      </div>'''

    return f'''
    <div class="hero-card">
      {thumbnail_html}

      <div class="hero-body">
        <div class="channel">{item.source}</div>
        <h2>{item.title_zh or item.title}</h2>
        <p class="summary">{item.summary}</p>
        <div class="tags">{render_tags(item.tags)}</div>
      </div>

      {expand_content}
    </div>'''


def render_item_card(item: FetchedItem, show_thumbnail: bool = True) -> str:
    """渲染普通内容卡片"""
    thumbnail_html = ""
    if show_thumbnail and item.thumbnail:
        duration_html = ""
        if item.extra.get("duration"):
            duration_html = f'<span class="duration">{item.extra["duration"]}</span>'
        thumbnail_html = f'''
      <div class="card-thumb">
        <img src="{item.extra.get('thumbnail_mq', item.thumbnail)}" alt="" onerror="this.parentElement.style.display='none'">
        {duration_html}
      </div>'''

    return f'''
    <a href="{item.link}" target="_blank" class="video-card">
      {thumbnail_html}
      <div class="card-info">
        <h3>{item.title_zh or item.title}</h3>
        <div class="meta">
          <span>{item.source}</span>
          <span class="dot">·</span>
          <span>{time_ago(item.pub_date)}</span>
        </div>
        <div class="tags">{render_tags(item.tags)}</div>
      </div>
    </a>'''


def render_compact_card(item: FetchedItem) -> str:
    """渲染紧凑卡片（无缩略图）"""
    return f'''
    <a href="{item.link}" target="_blank" class="compact-card">
      <div class="compact-info">
        <h3>{item.title_zh or item.title}</h3>
        <p class="compact-summary">{item.summary[:100] if item.summary else ''}</p>
        <div class="meta">
          <span>{item.source}</span>
          <span class="dot">·</span>
          <span>{time_ago(item.pub_date)}</span>
        </div>
        <div class="tags">{render_tags(item.tags)}</div>
      </div>
    </a>'''


def render_module_preview(module_name: str, module_name_zh: str, icon: str,
                          hero: FetchedItem, items: list[FetchedItem],
                          detail_page: str) -> str:
    """渲染模块预览（首页用）"""
    hero_html = ""
    if hero:
        hero_html = f'''
        <div class="preview-hero">
          <a href="{hero.link}" target="_blank">
            <h3>{hero.title_zh or hero.title}</h3>
          </a>
          <p>{hero.summary[:80] if hero.summary else ''}</p>
          <div class="tags">{render_tags(hero.tags)}</div>
        </div>'''

    items_html = ""
    for item in items[:2]:
        items_html += f'''
        <a href="{item.link}" target="_blank" class="preview-item">
          <span class="preview-title">{item.title_zh or item.title}</span>
          <span class="preview-source">{item.source}</span>
        </a>'''

    return f'''
    <div class="module-preview">
      <div class="module-header">
        <span class="module-icon">{icon}</span>
        <span class="module-name">{module_name_zh}</span>
        <a href="{detail_page}" class="module-more">查看全部 →</a>
      </div>
      {hero_html}
      <div class="preview-list">
        {items_html}
      </div>
    </div>'''
