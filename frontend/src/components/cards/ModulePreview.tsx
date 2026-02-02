import { Link } from 'react-router-dom'
import type { Item } from '../../types'

interface ModulePreviewProps {
  module: string
  moduleZh: string
  icon: string
  hero: Item | null
  items: Item[]
  onItemClick?: (item: Item) => void
}

export function ModulePreview({ module, moduleZh, icon, hero, items, onItemClick }: ModulePreviewProps) {
  const handleClick = (e: React.MouseEvent, item: Item) => {
    e.preventDefault()
    onItemClick?.(item)
  }

  return (
    <div className="module-preview">
      <div className="module-header">
        <span className="module-icon">{icon}</span>
        <span className="module-name">{moduleZh}</span>
        <Link to={`/${module}`} className="module-more">
          查看全部 →
        </Link>
      </div>

      {hero && (
        <div className="preview-hero" onClick={(e) => handleClick(e, hero)}>
          <h3>{hero.title}</h3>
        </div>
      )}

      {items.length > 0 && (
        <div className="preview-list">
          {items.slice(0, 2).map((item) => (
            <div
              key={item.id}
              className="preview-item"
              onClick={(e) => handleClick(e, item)}
            >
              <span className="preview-title">{item.title}</span>
              <span className="preview-source">{item.source}</span>
            </div>
          ))}
        </div>
      )}

      {!hero && items.length === 0 && (
        <div className="empty-state">
          <p>暂无内容</p>
        </div>
      )}
    </div>
  )
}
