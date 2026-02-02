import type { Item } from '../../types'
import { Tags } from '../common/Tag'
import { TimeAgo } from '../common/TimeAgo'

interface SubstackCardProps {
  item: Item
  onClick?: (item: Item) => void
}

// Source logos/colors
const SOURCE_CONFIG: Record<string, { color: string; icon: string; bgColor: string; logo?: string }> = {
  'OpenAI Blog': { color: '#10a37f', icon: '◯', bgColor: 'rgba(16, 163, 127, 0.1)', logo: 'https://openai.com/favicon.ico' },
  'Anthropic News': { color: '#d4a27f', icon: '◈', bgColor: 'rgba(212, 162, 127, 0.1)', logo: 'https://www.anthropic.com/favicon.ico' },
  'Google AI Blog': { color: '#4285f4', icon: 'G', bgColor: 'rgba(66, 133, 244, 0.1)', logo: 'https://www.gstatic.com/devrel-devsite/prod/v0e0f589edd85502a40d78d7d0825db8ea5ef3b99ab4070381ee86977c9168730/developers/images/favicon.png' },
  'Meta AI Blog': { color: '#0668e1', icon: 'M', bgColor: 'rgba(6, 104, 225, 0.1)', logo: 'https://ai.meta.com/favicon.ico' },
  'xAI News': { color: '#000000', icon: '𝕏', bgColor: 'rgba(0, 0, 0, 0.05)' },
  'Mistral AI News': { color: '#ff7000', icon: '▲', bgColor: 'rgba(255, 112, 0, 0.1)', logo: 'https://mistral.ai/favicon.ico' },
  'The Batch': { color: '#ff6719', icon: '📊', bgColor: 'rgba(255, 103, 25, 0.1)' },
  'Import AI': { color: '#7c3aed', icon: '📥', bgColor: 'rgba(124, 58, 237, 0.1)' },
  'One Useful Thing': { color: '#059669', icon: '💡', bgColor: 'rgba(5, 150, 105, 0.1)' },
  'Interconnects': { color: '#2563eb', icon: '🔗', bgColor: 'rgba(37, 99, 235, 0.1)' },
  'Ahead of AI': { color: '#dc2626', icon: '🚀', bgColor: 'rgba(220, 38, 38, 0.1)' },
  'ChinaTalk': { color: '#ef4444', icon: '🇨🇳', bgColor: 'rgba(239, 68, 68, 0.1)' },
  'AI Snake Oil': { color: '#f59e0b', icon: '🐍', bgColor: 'rgba(245, 158, 11, 0.1)' },
  "Ben's Bites": { color: '#8b5cf6', icon: '🍪', bgColor: 'rgba(139, 92, 246, 0.1)' },
  'Creator Economy': { color: '#ec4899', icon: '✨', bgColor: 'rgba(236, 72, 153, 0.1)' },
}

const DEFAULT_CONFIG = { color: '#6b7280', icon: '📝', bgColor: 'rgba(107, 114, 128, 0.1)' }

export function SubstackCard({ item, onClick }: SubstackCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  const config = SOURCE_CONFIG[item.source] || DEFAULT_CONFIG
  const isOfficial = item.extra?.type === 'official'
  const keyPoints = (item.extra?.key_points as string[]) || item.key_points || []
  const coreInsight = (item.extra?.core_insight as string) || item.core_insight || ''

  return (
    <div className="news-card" onClick={handleClick}>
      {/* 图片区域 */}
      <div className="news-card-image">
        {item.thumbnail ? (
          <img src={item.thumbnail} alt={item.title} />
        ) : (
          <div className="news-card-image-placeholder" style={{ background: `linear-gradient(135deg, ${config.bgColor} 0%, ${config.color}15 100%)` }}>
            <span style={{ color: config.color, fontSize: '32px' }}>{config.icon}</span>
          </div>
        )}
        {isOfficial && (
          <span className="news-card-badge official">Official</span>
        )}
      </div>

      {/* 内容区域 */}
      <div className="news-card-content">
        {/* 来源信息 */}
        <div className="news-card-source">
          <div
            className="news-source-icon"
            style={{ backgroundColor: config.bgColor, color: config.color }}
          >
            {config.icon}
          </div>
          <span className="news-source-name">{item.source}</span>
          <span className="news-source-dot">·</span>
          <TimeAgo date={item.pub_date} />
        </div>

        {/* 标题 */}
        <h3 className="news-card-title">{item.title_zh || item.title}</h3>

        {/* 摘要 */}
        {item.summary && (
          <p className="news-card-summary">{item.summary}</p>
        )}

        {/* 核心观点（如果有） */}
        {coreInsight && (
          <div className="news-card-insight">
            <span className="insight-icon">💡</span>
            <span className="insight-text">{coreInsight}</span>
          </div>
        )}

        {/* 关键要点预览（最多显示2条） */}
        {keyPoints.length > 0 && (
          <div className="news-card-points">
            {keyPoints.slice(0, 2).map((point, index) => (
              <div key={index} className="news-point-item">
                <span className="point-bullet">•</span>
                <span className="point-text">{point}</span>
              </div>
            ))}
            {keyPoints.length > 2 && (
              <span className="news-points-more">+{keyPoints.length - 2} more</span>
            )}
          </div>
        )}

        {/* 标签 */}
        {item.tags && item.tags.length > 0 && (
          <div className="news-card-tags">
            <Tags tags={item.tags} />
          </div>
        )}
      </div>
    </div>
  )
}

export function SubstackHeroCard({ item, onClick }: SubstackCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  const config = SOURCE_CONFIG[item.source] || DEFAULT_CONFIG
  const isOfficial = item.extra?.type === 'official'
  const keyPoints = (item.extra?.key_points as string[]) || item.key_points || []
  const coreInsight = (item.extra?.core_insight as string) || item.core_insight || ''

  return (
    <div className="news-hero-card" onClick={handleClick}>
      {/* 左侧：图片 */}
      <div className="news-hero-image">
        {item.thumbnail ? (
          <img src={item.thumbnail} alt={item.title} />
        ) : (
          <div className="news-hero-image-placeholder" style={{ background: `linear-gradient(135deg, ${config.color}20 0%, ${config.color}40 100%)` }}>
            <span style={{ color: config.color, fontSize: '64px' }}>{config.icon}</span>
          </div>
        )}
        {isOfficial && (
          <span className="news-card-badge official">Official Blog</span>
        )}
      </div>

      {/* 右侧：内容 */}
      <div className="news-hero-content">
        {/* 来源和时间 */}
        <div className="news-hero-meta">
          <div
            className="news-source-icon"
            style={{ backgroundColor: config.bgColor, color: config.color }}
          >
            {config.icon}
          </div>
          <span className="news-source-name">{item.source}</span>
          <span className="news-source-dot">·</span>
          <span className="news-author">by {item.author}</span>
          <span className="news-source-dot">·</span>
          <TimeAgo date={item.pub_date} />
        </div>

        {/* 标题 */}
        <h2 className="news-hero-title">{item.title_zh || item.title}</h2>

        {/* 摘要 */}
        {item.summary && (
          <p className="news-hero-summary">{item.summary}</p>
        )}

        {/* 核心观点 */}
        {coreInsight && (
          <div className="news-hero-insight">
            <div className="insight-header">
              <span className="insight-icon">💡</span>
              <span className="insight-label">核心观点</span>
            </div>
            <p className="insight-content">{coreInsight}</p>
          </div>
        )}

        {/* 关键要点 */}
        {keyPoints.length > 0 && (
          <div className="news-hero-points">
            <div className="points-header">
              <span className="points-icon">📌</span>
              <span className="points-label">关键要点</span>
            </div>
            <ul className="points-list">
              {keyPoints.map((point, index) => (
                <li key={index}>
                  <span className="point-number">{index + 1}</span>
                  <span className="point-text">{point}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 标签 */}
        {item.tags && item.tags.length > 0 && (
          <div className="news-hero-tags">
            <Tags tags={item.tags} />
          </div>
        )}

        {/* 操作按钮 */}
        <div className="news-hero-actions">
          <a
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="news-read-btn"
            onClick={(e) => e.stopPropagation()}
          >
            阅读原文
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
      </div>
    </div>
  )
}
