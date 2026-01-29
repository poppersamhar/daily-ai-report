import feedparser
import requests
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from config import (
    YOUTUBE_CHANNELS, MAX_DURATION_SECONDS, CHANNEL_WEIGHTS,
    ENTITY_WEIGHTS, ENTITY_PATTERNS
)

# API 配置 - 从环境变量读取
import os
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")


def fetch_youtube_rss(channel_id: str) -> list:
    """获取 YouTube 频道 RSS"""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(url)
    return feed.entries


def get_video_duration(video_id: str) -> int:
    """获取视频时长（秒）"""
    if not RAPIDAPI_KEY:
        return 0

    url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
    }
    params = {"videoId": video_id}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        data = resp.json()
        return int(data.get("lengthSeconds", 0))
    except Exception as e:
        print(f"获取时长失败 {video_id}: {e}")
        return 0


def format_duration(seconds: int) -> str:
    """格式化时长显示"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


def is_within_24h(date_str: str) -> bool:
    """判断是否在24小时内"""
    try:
        from dateutil import parser
        pub_date = parser.parse(date_str)
        now = datetime.now(pub_date.tzinfo)
        return (now - pub_date) < timedelta(hours=24)
    except:
        return False


def extract_entities(title: str) -> list:
    """从标题提取关键实体"""
    entities = []
    title_lower = title.lower()
    seen = set()

    for pattern, label, entity_type in ENTITY_PATTERNS:
        if re.search(pattern, title_lower) and label not in seen:
            entities.append({"label": label, "type": entity_type})
            seen.add(label)

    return entities


def calculate_fame_score(video: dict) -> int:
    """计算知名度分数"""
    score = 0
    channel = video.get("channel", "")
    title = video.get("title", "").lower()

    # 频道权重
    for name, weight in CHANNEL_WEIGHTS.items():
        if name.lower() in channel.lower():
            score += weight
            break

    # 关键词权重
    for keyword, weight in ENTITY_WEIGHTS.items():
        if keyword in title:
            score += weight

    return score


def call_deepseek(prompt: str) -> str:
    """调用 DeepSeek API"""
    if not DEEPSEEK_API_KEY:
        return ""

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        resp = requests.post(url, headers=headers, json=data, timeout=60)
        result = resp.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"DeepSeek API 调用失败: {e}")
        return ""


def select_hero_video(videos: list) -> dict:
    """AI 筛选头条视频"""
    if not videos:
        return None

    # 构建视频列表
    video_list = "\n".join([
        f"{i+1}. [{v['channel']}] {v['title']} (时长: {v['duration']}, ID: {v['video_id']})"
        for i, v in enumerate(videos)
    ])

    prompt = f"""你是一位严格的 AI 科技主编。从下方视频列表中选出 1 个最具价值的视频作为今日头条。

筛选标准（优先级从高到低）：
1. 涉及 OpenAI/Google/Anthropic/NVIDIA 等巨头的重大发布
2. 涉及 Sam Altman/Andrej Karpathy/Dario Amodei 等顶流人物
3. 涉及具体技术原理（Scaling Law, Agent, Transformer）
4. 时长越短越好（同等价值下优先选短视频）

视频列表：
{video_list}

只返回被选中视频的序号（如 1），不要任何解释。"""

    result = call_deepseek(prompt)

    try:
        idx = int(re.search(r'\d+', result).group()) - 1
        if 0 <= idx < len(videos):
            return videos[idx]
    except:
        pass

    # 默认返回第一个
    return videos[0] if videos else None


def translate_and_summarize(video: dict) -> dict:
    """翻译标题并生成摘要"""
    prompt = f"""将以下 YouTube 视频标题翻译成中文，并生成简短摘要。

原标题：{video['title']}
频道：{video['channel']}

输出 JSON 格式：
{{"title_zh": "中文标题", "summary": "一句话摘要（20-30字）"}}

只输出 JSON，不要其他内容。"""

    result = call_deepseek(prompt)

    try:
        # 清理 markdown 标记
        result = re.sub(r'```json\s*', '', result)
        result = re.sub(r'```\s*', '', result)
        data = json.loads(result.strip())
        video["title_zh"] = data.get("title_zh", video["title"])
        video["summary"] = data.get("summary", "")
    except:
        video["title_zh"] = video["title"]
        video["summary"] = ""

    return video


def process_hero_video(video: dict) -> dict:
    """处理头条视频 - 生成深度总结"""
    prompt = f"""你是一名资深 AI 研究员。根据以下视频信息生成深度总结。

视频标题：{video['title']}
频道：{video['channel']}

输出 JSON 格式：
{{
  "title_zh": "中文标题（简洁有力）",
  "summary": "60-80字中文摘要",
  "core_insight": "一句话核心认知",
  "key_points": ["要点1", "要点2", "要点3"]
}}

只输出 JSON，不要其他内容。"""

    result = call_deepseek(prompt)

    try:
        result = re.sub(r'```json\s*', '', result)
        result = re.sub(r'```\s*', '', result)
        data = json.loads(result.strip())
        video.update(data)
    except Exception as e:
        print(f"处理头条视频失败: {e}")
        video["title_zh"] = video["title"]
        video["summary"] = ""
        video["core_insight"] = ""
        video["key_points"] = []

    return video


def fetch_all_videos() -> list:
    """获取所有频道的视频"""
    all_videos = []

    for channel_id, channel_name in YOUTUBE_CHANNELS.items():
        print(f"获取频道: {channel_name}")
        entries = fetch_youtube_rss(channel_id)

        for entry in entries:
            # 检查是否在24小时内
            pub_date = entry.get("published", "")
            if not is_within_24h(pub_date):
                continue

            video_id = entry.get("yt_videoid", "")
            if not video_id:
                continue

            # 获取时长
            duration_seconds = get_video_duration(video_id)

            # 过滤超长视频
            if duration_seconds > MAX_DURATION_SECONDS:
                print(f"  跳过超长视频: {entry.get('title', '')[:30]}...")
                continue

            video = {
                "video_id": video_id,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "channel": channel_name,
                "pub_date": pub_date,
                "duration_seconds": duration_seconds,
                "duration": format_duration(duration_seconds) if duration_seconds else "N/A",
                "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                "thumbnail_mq": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
            }

            video["entities"] = extract_entities(video["title"])
            video["fame_score"] = calculate_fame_score(video)

            all_videos.append(video)
            print(f"  + {video['title'][:40]}...")

    return all_videos


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


def generate_html(hero_video: dict, other_videos: list) -> str:
    """生成 HTML 页面"""
    today = datetime.now().strftime("%Y年%m月%d日")

    # 生成标签 HTML
    def render_tags(entities):
        if not entities:
            return ""
        tags = []
        for e in entities[:3]:
            cls = "company" if e["type"] == "company" else "person"
            tags.append(f'<span class="tag {cls}">{e["label"]}</span>')
        return "".join(tags)

    # 生成要点列表
    def render_key_points(points):
        if not points:
            return ""
        return "".join([f"<li>{p}</li>" for p in points])

    # 生成普通视频卡片
    def render_video_cards(videos):
        cards = []
        for v in videos:
            cards.append(f'''
    <a href="{v['link']}" target="_blank" class="video-card">
      <div class="card-thumb">
        <img src="{v['thumbnail_mq']}" alt="">
        <span class="duration">{v['duration']}</span>
      </div>
      <div class="card-info">
        <h3>{v.get('title_zh', v['title'])}</h3>
        <div class="meta">
          <span>{v['channel']}</span>
          <span class="dot">·</span>
          <span>{time_ago(v['pub_date'])}</span>
        </div>
        <div class="tags">{render_tags(v['entities'])}</div>
      </div>
    </a>''')
        return "\n".join(cards)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>每日 AI 视频精选</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
      background: #f5f5f7;
      color: #1d1d1f;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }}

    .header {{
      background: linear-gradient(180deg, #e8f4fc 0%, #f5f5f7 100%);
      padding: 60px 20px 40px;
      text-align: center;
    }}

    .header-badge {{
      display: inline-block;
      background: #007aff;
      color: white;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      margin-bottom: 16px;
      letter-spacing: 0.5px;
    }}

    .header h1 {{
      font-size: 40px;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 8px;
      background: linear-gradient(90deg, #007aff, #5856d6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}

    .header p {{
      color: #86868b;
      font-size: 17px;
    }}

    .container {{
      max-width: 680px;
      margin: 0 auto;
      padding: 0 20px 60px;
    }}

    .section-title {{
      font-size: 24px;
      font-weight: 600;
      margin: 40px 0 20px;
      color: #1d1d1f;
    }}

    /* 头条卡片 */
    .hero-card {{
      background: white;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 4px 24px rgba(0, 122, 255, 0.08);
      border: 1px solid rgba(0, 122, 255, 0.1);
    }}

    .hero-thumb {{
      position: relative;
      width: 100%;
      aspect-ratio: 16/9;
      background: #000;
    }}

    .hero-thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    .hero-badge {{
      position: absolute;
      top: 16px;
      left: 16px;
      background: linear-gradient(135deg, #007aff, #5856d6);
      color: white;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 8px;
    }}

    .duration {{
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(0, 0, 0, 0.75);
      color: white;
      font-size: 13px;
      font-weight: 500;
      padding: 4px 8px;
      border-radius: 6px;
    }}

    .hero-body {{
      padding: 24px;
    }}

    .channel {{
      font-size: 14px;
      color: #007aff;
      font-weight: 500;
      margin-bottom: 8px;
    }}

    .hero-body h2 {{
      font-size: 22px;
      font-weight: 600;
      line-height: 1.3;
      margin-bottom: 12px;
    }}

    .summary {{
      font-size: 15px;
      color: #6e6e73;
      line-height: 1.6;
      margin-bottom: 16px;
    }}

    .tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .tag {{
      font-size: 12px;
      font-weight: 500;
      padding: 5px 12px;
      border-radius: 20px;
      background: #f5f5f7;
      color: #6e6e73;
    }}

    .tag.company {{
      background: #e8f4fc;
      color: #007aff;
    }}

    .tag.person {{
      background: #fef6e8;
      color: #bf5a00;
    }}

    /* 展开按钮 */
    .expand-btn {{
      width: 100%;
      padding: 16px;
      background: #f5f5f7;
      border: none;
      font-size: 15px;
      font-weight: 500;
      color: #007aff;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: background 0.2s;
    }}

    .expand-btn:hover {{
      background: #e8e8ed;
    }}

    .expand-btn .arrow {{
      transition: transform 0.3s;
    }}

    .expand-btn.active .arrow {{
      transform: rotate(180deg);
    }}

    /* 展开内容 */
    .expand-content {{
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.4s ease;
      background: #fafafa;
    }}

    .expand-content.active {{
      max-height: 1500px;
    }}

    .expand-inner {{
      padding: 24px;
    }}

    .insight-box {{
      background: white;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      border-left: 4px solid #007aff;
    }}

    .insight-label {{
      font-size: 12px;
      font-weight: 600;
      color: #007aff;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }}

    .insight-text {{
      font-size: 15px;
      color: #1d1d1f;
      font-weight: 500;
    }}

    .key-points {{
      list-style: none;
      margin-top: 16px;
    }}

    .key-points li {{
      position: relative;
      padding-left: 20px;
      margin-bottom: 10px;
      font-size: 14px;
      color: #6e6e73;
    }}

    .key-points li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 8px;
      width: 6px;
      height: 6px;
      background: #007aff;
      border-radius: 50%;
    }}

    .watch-btn {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 16px;
      background: #007aff;
      color: white;
      text-decoration: none;
      border-radius: 12px;
      font-size: 15px;
      font-weight: 600;
      transition: background 0.2s;
    }}

    .watch-btn:hover {{
      background: #0066d6;
    }}

    /* 普通视频卡片 */
    .video-card {{
      display: flex;
      background: white;
      border-radius: 16px;
      overflow: hidden;
      margin-bottom: 16px;
      text-decoration: none;
      color: inherit;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
      transition: transform 0.2s, box-shadow 0.2s;
    }}

    .video-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }}

    .card-thumb {{
      position: relative;
      width: 160px;
      min-width: 160px;
      height: 100px;
      background: #000;
    }}

    .card-thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    .card-thumb .duration {{
      bottom: 8px;
      right: 8px;
      font-size: 11px;
      padding: 3px 6px;
    }}

    .card-info {{
      flex: 1;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}

    .card-info h3 {{
      font-size: 15px;
      font-weight: 600;
      line-height: 1.4;
      margin-bottom: 6px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .meta {{
      font-size: 13px;
      color: #86868b;
      margin-bottom: 8px;
    }}

    .meta .dot {{
      margin: 0 6px;
    }}

    .card-info .tags {{
      gap: 6px;
    }}

    .card-info .tag {{
      font-size: 11px;
      padding: 3px 8px;
    }}

    /* 页脚 */
    .footer {{
      text-align: center;
      padding: 40px 20px;
      color: #86868b;
      font-size: 13px;
    }}

    .footer a {{
      color: #007aff;
      text-decoration: none;
    }}

    /* 空状态 */
    .empty-state {{
      text-align: center;
      padding: 60px 20px;
      color: #86868b;
    }}

    .empty-state .icon {{
      font-size: 48px;
      margin-bottom: 16px;
    }}

    @media (max-width: 600px) {{
      .header h1 {{
        font-size: 32px;
      }}

      .card-thumb {{
        width: 120px;
        min-width: 120px;
        height: 80px;
      }}

      .card-info h3 {{
        font-size: 14px;
      }}
    }}
  </style>
</head>
<body>

  <div class="header">
    <span class="header-badge">YouTube 精选</span>
    <h1>每日 AI 视频</h1>
    <p>{today} · 精选内容</p>
  </div>

  <div class="container">
'''

    # 头条视频
    if hero_video:
        html += f'''
    <div class="section-title">今日精选</div>

    <div class="hero-card">
      <div class="hero-thumb">
        <span class="hero-badge">精选推荐</span>
        <img src="{hero_video['thumbnail']}" alt="">
        <span class="duration">{hero_video['duration']}</span>
      </div>

      <div class="hero-body">
        <div class="channel">{hero_video['channel']}</div>
        <h2>{hero_video.get('title_zh', hero_video['title'])}</h2>
        <p class="summary">{hero_video.get('summary', '')}</p>
        <div class="tags">{render_tags(hero_video['entities'])}</div>
      </div>

      <button class="expand-btn" onclick="toggleExpand(this)">
        <span>查看详情</span>
        <span class="arrow">▼</span>
      </button>

      <div class="expand-content">
        <div class="expand-inner">
          <div class="insight-box">
            <div class="insight-label">核心观点</div>
            <div class="insight-text">{hero_video.get('core_insight', '')}</div>
            <ul class="key-points">
              {render_key_points(hero_video.get('key_points', []))}
            </ul>
          </div>

          <a href="{hero_video['link']}" target="_blank" class="watch-btn">
            观看原视频
          </a>
        </div>
      </div>
    </div>
'''

    # 更多视频
    if other_videos:
        html += f'''
    <div class="section-title">更多视频</div>
    {render_video_cards(other_videos)}
'''

    # 空状态
    if not hero_video and not other_videos:
        html += '''
    <div class="empty-state">
      <div class="icon">📺</div>
      <p>暂无最新视频</p>
    </div>
'''

    html += '''
  </div>

  <div class="footer">
    <p>Daily AI Report · 每日自动更新</p>
  </div>

  <script>
    function toggleExpand(btn) {
      btn.classList.toggle('active');
      btn.nextElementSibling.classList.toggle('active');
    }
  </script>

</body>
</html>'''

    return html


def main():
    print("=" * 50)
    print("每日 AI 视频精选 - 开始运行")
    print("=" * 50)

    # 1. 获取所有视频
    print("\n[1/4] 获取视频列表...")
    videos = fetch_all_videos()
    print(f"共获取 {len(videos)} 个视频")

    if not videos:
        print("没有找到24小时内的新视频")
        # 生成空页面
        html = generate_html(None, [])
        output_path = Path(__file__).parent / "index.html"
        output_path.write_text(html, encoding="utf-8")
        print(f"已生成空页面: {output_path}")
        return

    # 2. AI 筛选头条
    print("\n[2/4] AI 筛选头条视频...")
    hero_video = select_hero_video(videos)
    if hero_video:
        print(f"头条: {hero_video['title'][:40]}...")

    # 3. 处理视频
    print("\n[3/4] 处理视频内容...")

    # 处理头条视频
    if hero_video:
        hero_video = process_hero_video(hero_video)

    # 处理其他视频（按知名度排序）
    other_videos = [v for v in videos if v.get("video_id") != hero_video.get("video_id")]
    other_videos.sort(key=lambda x: x.get("fame_score", 0), reverse=True)

    # 翻译其他视频标题
    for v in other_videos[:10]:  # 最多处理10个
        translate_and_summarize(v)

    # 4. 生成 HTML
    print("\n[4/4] 生成 HTML 页面...")
    html = generate_html(hero_video, other_videos[:10])

    output_path = Path(__file__).parent / "index.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"\n完成！输出文件: {output_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
