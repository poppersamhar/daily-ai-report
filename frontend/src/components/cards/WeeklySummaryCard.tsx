import type { WeeklySummary } from '../../types'

interface WeeklySummaryCardProps {
  summary: WeeklySummary
}

export function WeeklySummaryCard({ summary }: WeeklySummaryCardProps) {
  const formatDateRange = () => {
    const start = new Date(summary.week_start)
    const end = new Date(summary.week_end)
    return `${start.getMonth() + 1}/${start.getDate()} - ${end.getMonth() + 1}/${end.getDate()}`
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case '上升': return '↑'
      case '下降': return '↓'
      default: return '→'
    }
  }

  const getTrendClass = (trend: string) => {
    switch (trend) {
      case '上升': return 'trend-up'
      case '下降': return 'trend-down'
      default: return 'trend-flat'
    }
  }

  return (
    <div className="weekly-summary-card">
      <div className="weekly-summary-header">
        <div className="weekly-summary-badge">AI 周报</div>
        <span className="weekly-summary-date">{formatDateRange()}</span>
      </div>

      <h2 className="weekly-summary-headline">{summary.headline}</h2>

      <div className="weekly-summary-section">
        <h3>热点话题</h3>
        <div className="hot-topics-list">
          {summary.hot_topics.map((topic, idx) => (
            <div key={idx} className="hot-topic-item">
              <div className="hot-topic-header">
                <span className="hot-topic-name">{topic.topic}</span>
                <span className={`hot-topic-trend ${getTrendClass(topic.trend)}`}>
                  {getTrendIcon(topic.trend)} {topic.trend}
                </span>
              </div>
              <p className="hot-topic-desc">{topic.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="weekly-summary-section">
        <h3>重要事件</h3>
        <div className="key-events-list">
          {summary.key_events.map((event, idx) => (
            <div key={idx} className="key-event-item">
              <span className="key-event-title">{event.title}</span>
              <p className="key-event-summary">{event.summary}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="weekly-summary-section">
        <h3>趋势分析</h3>
        <p className="trend-analysis-text">{summary.trend_analysis}</p>
      </div>

      {Object.keys(summary.company_mentions).length > 0 && (
        <div className="weekly-summary-section">
          <h3>公司热度</h3>
          <div className="company-mentions">
            {Object.entries(summary.company_mentions)
              .sort(([, a], [, b]) => b - a)
              .slice(0, 6)
              .map(([company, count]) => (
                <span key={company} className="company-tag">
                  {company} <span className="company-count">{count}</span>
                </span>
              ))}
          </div>
        </div>
      )}

      <div className="weekly-summary-footer">
        <span>本周共收录 {summary.total_items} 条内容</span>
      </div>
    </div>
  )
}
