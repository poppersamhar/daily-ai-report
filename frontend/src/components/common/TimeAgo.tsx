interface TimeAgoProps {
  date: string
}

export function TimeAgo({ date }: TimeAgoProps) {
  if (!date) return null

  const getTimeAgo = (dateStr: string): string => {
    try {
      const pubDate = new Date(dateStr)
      const now = new Date()
      const diffMs = now.getTime() - pubDate.getTime()
      const hours = Math.floor(diffMs / (1000 * 60 * 60))

      if (hours < 1) return '刚刚'
      if (hours < 24) return `${hours}小时前`
      return `${Math.floor(hours / 24)}天前`
    } catch {
      return ''
    }
  }

  return <span>{getTimeAgo(date)}</span>
}
