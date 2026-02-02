import type { Item } from '../../types'
import { TimeAgo } from '../common/TimeAgo'

interface CompactCardProps {
  item: Item
  onClick?: (item: Item) => void
}

export function CompactCard({ item, onClick }: CompactCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  return (
    <div className="compact-card" onClick={handleClick}>
      <div className="compact-info">
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
