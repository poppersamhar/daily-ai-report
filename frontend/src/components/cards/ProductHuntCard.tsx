import type { Item } from '../../types'

interface ProductHuntCardProps {
  item: Item
  rank?: number
  onClick?: (item: Item) => void
}

export function ProductHuntCard({ item, rank, onClick }: ProductHuntCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  const upvotes = (item.extra?.upvotes as number) || 0
  const comments = (item.extra?.comments as number) || 0
  const tagline = (item.extra?.tagline as string) || item.summary
  const topics = (item.extra?.topics as string[]) || []

  // 生成渐变背景色
  const gradientColors = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
  ]
  const bgGradient = gradientColors[(rank || 1) % gradientColors.length]

  return (
    <div className="ph-card" onClick={handleClick}>
      {/* 排名徽章 */}
      {rank && (
        <div className="ph-rank">
          <span className="ph-rank-number">#{rank}</span>
        </div>
      )}

      {/* 产品图片/Logo */}
      <div className="ph-card-image">
        {item.thumbnail ? (
          <img src={item.thumbnail} alt={item.title} />
        ) : (
          <div className="ph-card-image-placeholder" style={{ background: bgGradient }}>
            <span className="ph-card-initial">{item.title.charAt(0).toUpperCase()}</span>
          </div>
        )}
      </div>

      {/* 内容区域 */}
      <div className="ph-card-content">
        {/* 产品名称 */}
        <h3 className="ph-card-title">{item.title}</h3>

        {/* Tagline */}
        <p className="ph-card-tagline">{tagline}</p>

        {/* 中文介绍 */}
        {item.title_zh && item.title_zh !== item.title && (
          <p className="ph-card-summary">{item.title_zh}</p>
        )}

        {/* 标签 */}
        {topics.length > 0 && (
          <div className="ph-card-topics">
            {topics.slice(0, 3).map((topic, index) => (
              <span key={index} className="ph-topic-tag">{topic}</span>
            ))}
          </div>
        )}
      </div>

      {/* 底部统计 */}
      <div className="ph-card-footer">
        {/* Upvotes */}
        <div className="ph-upvote">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 19V5M5 12l7-7 7 7"/>
          </svg>
          <span className="ph-upvote-count">{upvotes.toLocaleString()}</span>
        </div>

        {/* Comments */}
        <div className="ph-comments">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          <span>{comments}</span>
        </div>

        {/* 访问链接 */}
        <a
          href={item.link}
          target="_blank"
          rel="noopener noreferrer"
          className="ph-visit-btn"
          onClick={(e) => e.stopPropagation()}
        >
          Visit
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15 3 21 3 21 9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
        </a>
      </div>
    </div>
  )
}

export function ProductHuntHeroCard({ item, onClick }: ProductHuntCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  const upvotes = (item.extra?.upvotes as number) || 0
  const comments = (item.extra?.comments as number) || 0
  const tagline = (item.extra?.tagline as string) || item.summary
  const topics = (item.extra?.topics as string[]) || []

  return (
    <div className="ph-hero-card" onClick={handleClick}>
      {/* 左侧：产品图片 */}
      <div className="ph-hero-image">
        {item.thumbnail ? (
          <img src={item.thumbnail} alt={item.title} />
        ) : (
          <div className="ph-hero-image-placeholder">
            <span className="ph-hero-initial">{item.title.charAt(0).toUpperCase()}</span>
          </div>
        )}
        <span className="ph-hero-badge">#1 Product of the Week</span>
      </div>

      {/* 右侧：内容 */}
      <div className="ph-hero-content">
        <div className="ph-hero-meta">
          <span className="ph-source">Product Hunt</span>
          <span className="ph-dot">·</span>
          <span className="ph-author">by {item.author}</span>
        </div>

        <h2 className="ph-hero-title">{item.title}</h2>
        <p className="ph-hero-tagline">{tagline}</p>

        {item.title_zh && item.title_zh !== item.title && (
          <p className="ph-hero-summary">{item.title_zh}</p>
        )}

        {/* 统计数据 */}
        <div className="ph-hero-stats">
          <div className="ph-stat">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 19V5M5 12l7-7 7 7"/>
            </svg>
            <strong>{upvotes.toLocaleString()}</strong>
            <span>upvotes</span>
          </div>
          <div className="ph-stat">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <strong>{comments}</strong>
            <span>comments</span>
          </div>
        </div>

        {/* 标签 */}
        {topics.length > 0 && (
          <div className="ph-hero-topics">
            {topics.map((topic, index) => (
              <span key={index} className="ph-topic-tag">{topic}</span>
            ))}
          </div>
        )}

        {/* 操作按钮 */}
        <div className="ph-hero-actions">
          <a
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="ph-primary-btn"
            onClick={(e) => e.stopPropagation()}
          >
            Visit Product
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
              <polyline points="15 3 21 3 21 9"/>
              <line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
  )
}
