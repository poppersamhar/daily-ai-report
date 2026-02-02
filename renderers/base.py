from datetime import datetime


def get_base_styles() -> str:
    """获取基础 CSS 样式"""
    return '''
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
      background: #f5f5f7;
      color: #1d1d1f;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    a {
      text-decoration: none;
      color: inherit;
    }

    /* 导航栏 */
    .navbar {
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(0, 0, 0, 0.1);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .nav-inner {
      max-width: 100%;
      margin: 0;
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .nav-brand {
      font-size: 18px;
      font-weight: 600;
      color: #1d1d1f;
    }

    .nav-links {
      display: flex;
      gap: 24px;
    }

    .nav-link {
      font-size: 14px;
      color: #6e6e73;
      transition: color 0.2s;
    }

    .nav-link:hover,
    .nav-link.active {
      color: #007aff;
    }

    /* 头部 */
    .header {
      background: linear-gradient(180deg, #e8f4fc 0%, #f5f5f7 100%);
      padding: 60px 20px 40px;
      text-align: center;
    }

    .header-badge {
      display: inline-block;
      background: #007aff;
      color: white;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      margin-bottom: 16px;
      letter-spacing: 0.5px;
    }

    .header h1 {
      font-size: 40px;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 8px;
      background: linear-gradient(90deg, #007aff, #5856d6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .header p {
      color: #86868b;
      font-size: 17px;
    }

    .container {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 20px 60px;
    }

    .section-title {
      font-size: 24px;
      font-weight: 600;
      margin: 40px 0 20px;
      color: #1d1d1f;
    }

    /* 头条卡片 */
    .hero-card {
      background: white;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 4px 24px rgba(0, 122, 255, 0.08);
      border: 1px solid rgba(0, 122, 255, 0.1);
      margin-bottom: 24px;
    }

    .hero-thumb {
      position: relative;
      width: 100%;
      aspect-ratio: 16/9;
      background: #000;
    }

    .hero-thumb img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .hero-badge {
      position: absolute;
      top: 16px;
      left: 16px;
      background: linear-gradient(135deg, #007aff, #5856d6);
      color: white;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 8px;
    }

    .duration {
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(0, 0, 0, 0.75);
      color: white;
      font-size: 13px;
      font-weight: 500;
      padding: 4px 8px;
      border-radius: 6px;
    }

    .hero-body {
      padding: 24px;
    }

    .channel {
      font-size: 14px;
      color: #007aff;
      font-weight: 500;
      margin-bottom: 8px;
    }

    .hero-body h2 {
      font-size: 22px;
      font-weight: 600;
      line-height: 1.3;
      margin-bottom: 12px;
    }

    .summary {
      font-size: 15px;
      color: #6e6e73;
      line-height: 1.6;
      margin-bottom: 16px;
    }

    /* 标签 */
    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .tag {
      font-size: 12px;
      font-weight: 500;
      padding: 5px 12px;
      border-radius: 20px;
      background: #f5f5f7;
      color: #6e6e73;
    }

    .tag.company {
      background: #e8f4fc;
      color: #007aff;
    }

    .tag.person {
      background: #fef6e8;
      color: #bf5a00;
    }

    .tag.topic, .tag.tech {
      background: #f0e8fc;
      color: #5856d6;
    }

    .tag.event {
      background: #e8fcf0;
      color: #00a86b;
    }

    .tag.lang {
      background: #fce8e8;
      color: #d63031;
    }

    /* 展开按钮 */
    .expand-btn {
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
    }

    .expand-btn:hover {
      background: #e8e8ed;
    }

    .expand-btn .arrow {
      transition: transform 0.3s;
    }

    .expand-btn.active .arrow {
      transform: rotate(180deg);
    }

    /* 展开内容 */
    .expand-content {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.4s ease;
      background: #fafafa;
    }

    .expand-content.active {
      max-height: 1500px;
    }

    .expand-inner {
      padding: 24px;
    }

    .insight-box {
      background: white;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      border-left: 4px solid #007aff;
    }

    .insight-label {
      font-size: 12px;
      font-weight: 600;
      color: #007aff;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }

    .insight-text {
      font-size: 15px;
      color: #1d1d1f;
      font-weight: 500;
    }

    .key-points {
      list-style: none;
      margin-top: 16px;
    }

    .key-points li {
      position: relative;
      padding-left: 20px;
      margin-bottom: 10px;
      font-size: 14px;
      color: #6e6e73;
    }

    .key-points li::before {
      content: "";
      position: absolute;
      left: 0;
      top: 8px;
      width: 6px;
      height: 6px;
      background: #007aff;
      border-radius: 50%;
    }

    .watch-btn {
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
    }

    .watch-btn:hover {
      background: #0066d6;
    }

    /* 普通卡片 */
    .video-card {
      display: flex;
      background: white;
      border-radius: 16px;
      overflow: hidden;
      margin-bottom: 16px;
      text-decoration: none;
      color: inherit;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .video-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    .card-thumb {
      position: relative;
      width: 160px;
      min-width: 160px;
      height: 100px;
      background: #f0f0f0;
    }

    .card-thumb img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .card-thumb .duration {
      bottom: 8px;
      right: 8px;
      font-size: 11px;
      padding: 3px 6px;
    }

    .card-info {
      flex: 1;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .card-info h3 {
      font-size: 15px;
      font-weight: 600;
      line-height: 1.4;
      margin-bottom: 6px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .meta {
      font-size: 13px;
      color: #86868b;
      margin-bottom: 8px;
    }

    .meta .dot {
      margin: 0 6px;
    }

    .card-info .tags {
      gap: 6px;
    }

    .card-info .tag {
      font-size: 11px;
      padding: 3px 8px;
    }

    /* 紧凑卡片 */
    .compact-card {
      display: block;
      background: white;
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .compact-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }

    .compact-info h3 {
      font-size: 15px;
      font-weight: 600;
      line-height: 1.4;
      margin-bottom: 8px;
    }

    .compact-summary {
      font-size: 14px;
      color: #6e6e73;
      line-height: 1.5;
      margin-bottom: 8px;
    }

    /* 模块预览 */
    .modules-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-top: 30px;
      max-width: 900px;
      margin-left: auto;
      margin-right: auto;
    }

    .module-preview {
      background: white;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }

    .module-header {
      display: flex;
      align-items: center;
      margin-bottom: 16px;
    }

    .module-icon {
      font-size: 20px;
      margin-right: 8px;
    }

    .module-name {
      font-size: 16px;
      font-weight: 600;
      flex: 1;
    }

    .module-more {
      font-size: 13px;
      color: #007aff;
    }

    .preview-hero h3 {
      font-size: 15px;
      font-weight: 600;
      line-height: 1.4;
      margin-bottom: 8px;
      color: #1d1d1f;
    }

    .preview-hero h3:hover {
      color: #007aff;
    }

    .preview-hero p {
      font-size: 13px;
      color: #6e6e73;
      margin-bottom: 10px;
    }

    .preview-list {
      margin-top: 16px;
      border-top: 1px solid #f0f0f0;
      padding-top: 12px;
    }

    .preview-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-bottom: 1px solid #f5f5f5;
    }

    .preview-item:last-child {
      border-bottom: none;
    }

    .preview-title {
      font-size: 13px;
      color: #1d1d1f;
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      margin-right: 12px;
    }

    .preview-source {
      font-size: 12px;
      color: #86868b;
      white-space: nowrap;
    }

    /* 页脚 */
    .footer {
      text-align: center;
      padding: 40px 20px;
      color: #86868b;
      font-size: 13px;
    }

    .footer a {
      color: #007aff;
      text-decoration: none;
    }

    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: #86868b;
    }

    .empty-state .icon {
      font-size: 48px;
      margin-bottom: 16px;
    }

    /* 响应式 */
    @media (max-width: 768px) {
      .modules-grid {
        grid-template-columns: 1fr;
      }

      .nav-links {
        display: none;
      }
    }

    @media (max-width: 600px) {
      .header h1 {
        font-size: 32px;
      }

      .card-thumb {
        width: 120px;
        min-width: 120px;
        height: 80px;
      }

      .card-info h3 {
        font-size: 14px;
      }
    }
'''


def get_base_script() -> str:
    """获取基础 JavaScript"""
    return '''
    function toggleExpand(btn) {
      btn.classList.toggle('active');
      btn.nextElementSibling.classList.toggle('active');
    }
'''


def render_navbar(active_page: str = "index") -> str:
    """渲染导航栏"""
    pages = [
        ("index", "首页", "index.html"),
        ("youtube", "YouTube", "youtube.html"),
        ("substack", "Substack", "substack.html"),
        ("twitter", "Twitter", "twitter.html"),
        ("products", "产品", "products.html"),
        ("business", "商业", "business.html"),
    ]

    links = []
    for page_id, name, url in pages:
        active_class = " active" if page_id == active_page else ""
        links.append(f'<a href="{url}" class="nav-link{active_class}">{name}</a>')

    return f'''
  <nav class="navbar">
    <div class="nav-inner">
      <a href="index.html" class="nav-brand">Daily AI Report</a>
      <div class="nav-links">
        {"".join(links)}
      </div>
    </div>
  </nav>'''


def render_header(title: str, subtitle: str, badge: str = "") -> str:
    """渲染页面头部"""
    today = datetime.now().strftime("%Y年%m月%d日")
    badge_html = f'<span class="header-badge">{badge}</span>' if badge else ""

    return f'''
  <div class="header">
    {badge_html}
    <h1>{title}</h1>
    <p>{today} · {subtitle}</p>
  </div>'''


def render_footer() -> str:
    """渲染页脚"""
    return '''
  <div class="footer">
    <p>Daily AI Report · 每日自动更新</p>
  </div>'''


def wrap_html(content: str, title: str = "Daily AI Report",
              active_page: str = "index", extra_styles: str = "") -> str:
    """包装完整 HTML 页面"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    {get_base_styles()}
    {extra_styles}
  </style>
</head>
<body>

  {render_navbar(active_page)}

  {content}

  {render_footer()}

  <script>
    {get_base_script()}
  </script>

</body>
</html>'''
