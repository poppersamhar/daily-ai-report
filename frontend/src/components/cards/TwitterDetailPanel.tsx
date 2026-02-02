import { useEffect } from 'react'
import type { Item } from '../../types'
import { Tags } from '../common/Tag'
import { DetailContext } from '../../App'

interface TwitterDetailPanelProps {
  item: Item | null
  onClose: () => void
}

export function TwitterDetailPanel({ item, onClose }: TwitterDetailPanelProps) {
  const tweetId = item?.extra?.tweet_id as string || (item?.id?.startsWith('twitter_') ? item.id.replace('twitter_', '') : null)

  // 控制页面缩放
  useEffect(() => {
    DetailContext.setOpen(!!item)
    return () => DetailContext.setOpen(false)
  }, [item])

  // 加载 Twitter widgets
  useEffect(() => {
    if (item && tweetId) {
      // @ts-ignore
      if (window.twttr && window.twttr.widgets) {
        setTimeout(() => {
          // @ts-ignore
          window.twttr.widgets.load()
        }, 100)
      }
    }
  }, [item, tweetId])

  if (!item) return null

  return (
    <>
      <div className="detail-overlay" onClick={onClose} />
      <div className="detail-panel">
        <div className="detail-header">
          <button className="detail-close" onClick={onClose}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div className="detail-content">
          {/* 摘要 */}
          {item.summary && (
            <div className="detail-section">
              <div className="section-label">摘要</div>
              <p className="section-text">{item.summary}</p>
            </div>
          )}

          {/* 翻译 */}
          {item.title_zh && item.title_zh !== item.title && (
            <div className="detail-section">
              <div className="section-label">翻译</div>
              <p className="section-text">{item.title_zh}</p>
            </div>
          )}

          {/* 核心认知 */}
          {item.core_insight && (
            <div className="detail-section">
              <div className="section-label">核心认知</div>
              <p className="section-text">{item.core_insight}</p>
            </div>
          )}

          {/* 关键要点 */}
          {item.key_points && item.key_points.length > 0 && (
            <div className="detail-section">
              <div className="section-label">关键要点</div>
              <ul className="detail-points">
                {item.key_points.map((point, index) => (
                  <li key={index}>{point}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Twitter 嵌入 */}
          <div className="detail-card">
            {tweetId && (
              <div className="detail-tweet">
                <blockquote className="twitter-tweet" data-theme="light">
                  <a href={`https://twitter.com/x/status/${tweetId}`}></a>
                </blockquote>
              </div>
            )}

            <div className="detail-meta">
              <Tags tags={item.tags} />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
