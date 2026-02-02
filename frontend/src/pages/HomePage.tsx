import { Link } from 'react-router-dom'
import { useWeeklySummary } from '../hooks/useModules'
import { WeeklySummaryCard } from '../components/cards/WeeklySummaryCard'

const FEATURES = [
  { label: '全球 AI 信源聚合' },
  { label: 'AI 智能翻译摘要' },
  { label: '周报自动生成' },
]

const MODULES = [
  { id: 'youtube', icon: '📺', name: 'YouTube', desc: 'AI 领域顶级频道' },
  { id: 'substack', icon: '📝', name: 'News', desc: '官方博客与 Newsletter' },
  { id: 'twitter', icon: '𝕏', name: 'Social', desc: 'X / Twitter & Reddit' },
  { id: 'products', icon: '🚀', name: 'Product', desc: 'GitHub Trending' },
  { id: 'podcast', icon: '🎧', name: '中文播客', desc: 'AI 深度访谈' },
]

export default function HomePage() {
  const { data: summaryData, isLoading } = useWeeklySummary()

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="brand-name">Zerde</span>
            <br />
            让 AI 洞察<span className="highlight">触手可及</span>
          </h1>

          <p className="hero-desc">
            为 AI 从业者打造的一站式信息聚合平台。
            <strong>全球信源实时聚合、AI 智能翻译摘要、周报自动生成</strong>，
            用 AI 提升信息获取效率，洞察行业前沿。
          </p>

          <div className="hero-features">
            {FEATURES.map((feature, index) => (
              <span key={index} className="feature-tag">
                {feature.label}
              </span>
            ))}
          </div>

          <div className="hero-actions">
            <Link to="/substack" className="btn-primary">
              立即探索
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </Link>
            <a href="#modules" className="btn-secondary">
              <span className="btn-icon">📖</span>
              查看模块
            </a>
          </div>
        </div>

        <div className="hero-visual">
          <div className="visual-card">
            <div className="visual-header">
              <span className="visual-dot red"></span>
              <span className="visual-dot yellow"></span>
              <span className="visual-dot green"></span>
            </div>
            <div className="visual-content">
              <div className="visual-item">
                <span className="visual-icon">📰</span>
                <div className="visual-text">
                  <span className="visual-title">OpenAI 发布 GPT-5</span>
                  <span className="visual-meta">2 小时前 · OpenAI Blog</span>
                </div>
              </div>
              <div className="visual-item">
                <span className="visual-icon">🔬</span>
                <div className="visual-text">
                  <span className="visual-title">Anthropic Claude 新突破</span>
                  <span className="visual-meta">5 小时前 · Anthropic</span>
                </div>
              </div>
              <div className="visual-item">
                <span className="visual-icon">🚀</span>
                <div className="visual-text">
                  <span className="visual-title">LangChain v0.3 发布</span>
                  <span className="visual-meta">1 天前 · GitHub</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Modules Section */}
      <section id="modules" className="modules-section">
        <div className="section-header">
          <span className="section-badge">数据模块</span>
          <h2 className="section-title-large">覆盖 AI 领域核心信源</h2>
          <p className="section-desc">从 YouTube 到播客，从 Twitter 到 GitHub，一站式获取 AI 领域最新动态</p>
        </div>

        <div className="modules-grid-home">
          {MODULES.map((module) => (
            <Link key={module.id} to={`/${module.id}`} className="module-card-home">
              <span className="module-icon-large">{module.icon}</span>
              <h3 className="module-name-home">{module.name}</h3>
              <p className="module-desc-home">{module.desc}</p>
              <span className="module-arrow">→</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Weekly Summary Section */}
      {summaryData?.data && (
        <section className="summary-section">
          <div className="section-header">
            <span className="section-badge">AI 周报</span>
            <h2 className="section-title-large">本周 AI 领域要闻</h2>
            <p className="section-desc">AI 自动生成的周度总结，快速了解行业动态</p>
          </div>

          <div className="container">
            {isLoading ? (
              <div className="loading">
                <div className="loading-spinner"></div>
                <p>Loading...</p>
              </div>
            ) : (
              <WeeklySummaryCard summary={summaryData.data} />
            )}
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <span className="section-badge">核心能力</span>
          <h2 className="section-title-large">为什么选择 Zerde</h2>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-card-icon">🌐</div>
            <h3>全球信源聚合</h3>
            <p>自动抓取 YouTube、Substack、Twitter、GitHub 等平台的 AI 相关内容，覆盖视频、文章、播客、开源项目等多种形式。</p>
          </div>

          <div className="feature-card">
            <div className="feature-card-icon">🤖</div>
            <h3>AI 智能处理</h3>
            <p>使用 DeepSeek 等大模型自动翻译英文内容、提取核心观点、生成摘要，让你快速获取关键信息。</p>
          </div>

          <div className="feature-card">
            <div className="feature-card-icon">📊</div>
            <h3>周报自动生成</h3>
            <p>每周自动汇总热点话题、关键事件、趋势分析，一份报告掌握 AI 领域全貌。</p>
          </div>

          <div className="feature-card">
            <div className="feature-card-icon">⚡</div>
            <h3>实时更新</h3>
            <p>定时任务自动抓取最新内容，确保你始终获取最新的 AI 行业动态。</p>
          </div>
        </div>
      </section>
    </div>
  )
}
