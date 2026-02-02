import { useState } from 'react'
import type { Item } from '../../types'
import { Tags } from '../common/Tag'

interface HeroCardProps {
  item: Item
  moduleIcon?: string
}

export function HeroCard({ item, moduleIcon }: HeroCardProps) {
  const [expanded, setExpanded] = useState(false)

  const duration = item.extra?.duration as string | undefined
  const hasThumbnail = !!item.thumbnail

  return (
    <div className="hero-card">
      {hasThumbnail && (
        <div className="hero-thumb">
          <img src={item.thumbnail} alt={item.title} />
          <span className="hero-badge">
            {moduleIcon} Featured
          </span>
          {duration && <span className="duration">{duration}</span>}
        </div>
      )}

      <div className="hero-body">
        <div className="channel">{item.source}</div>
        <h2>{item.title_zh || item.title}</h2>
        {item.summary && <p className="summary">{item.summary}</p>}
        <Tags tags={item.tags} />
      </div>

      {(item.core_insight || (item.key_points && item.key_points.length > 0)) && (
        <>
          <button
            className={`expand-btn${expanded ? ' active' : ''}`}
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? '收起' : '展开详情'}
            <span className="arrow">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </button>

          <div className={`expand-content${expanded ? ' active' : ''}`}>
            <div className="expand-inner">
              {item.core_insight && (
                <div className="insight-box">
                  <div className="insight-label">Core Insight</div>
                  <div className="insight-text">{item.core_insight}</div>
                </div>
              )}

              {item.key_points && item.key_points.length > 0 && (
                <ul className="key-points">
                  {item.key_points.map((point, index) => (
                    <li key={index}>{point}</li>
                  ))}
                </ul>
              )}

              <a
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
                className="watch-btn"
              >
                查看原文
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </>
      )}

      {!item.core_insight && (!item.key_points || item.key_points.length === 0) && (
        <div style={{ padding: '0 24px 24px' }}>
          <a
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="watch-btn"
          >
            查看原文
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
      )}
    </div>
  )
}
