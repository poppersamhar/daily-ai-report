import type { Item } from '../../types'
import { TimeAgo } from '../common/TimeAgo'

interface ItemCardProps {
  item: Item
  showThumbnail?: boolean
  onClick?: (item: Item) => void
}

export function ItemCard({ item, showThumbnail = true, onClick }: ItemCardProps) {
  const duration = item.extra?.duration as string | undefined
  const hasThumbnail = showThumbnail && !!item.thumbnail

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  return (
    <div className="video-card" onClick={handleClick}>
      {hasThumbnail && (
        <div className="card-thumb">
          <img src={item.thumbnail} alt={item.title} />
          {duration && <span className="duration">{duration}</span>}
        </div>
      )}

      <div className="card-info">
        <h3>{item.title}</h3>
        <div className="meta">
          <span>{item.source}</span>
          {item.pub_date && (
            <>
              <span className="dot">·</span>
              <TimeAgo date={item.pub_date} />
            </>
          )}
        </div>
      </div>
    </div>
  )
}
