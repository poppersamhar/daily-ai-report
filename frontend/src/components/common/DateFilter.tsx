interface DateFilterProps {
  value: number
  onChange: (days: number) => void
}

const OPTIONS = [
  { value: 1, label: '今天' },
  { value: 3, label: '3天' },
  { value: 7, label: '7天' },
]

export function DateFilter({ value, onChange }: DateFilterProps) {
  return (
    <div className="date-filter">
      <span className="date-filter-label">时间范围:</span>
      <div className="date-filter-options">
        {OPTIONS.map((option) => (
          <button
            key={option.value}
            className={`date-filter-btn ${value === option.value ? 'active' : ''}`}
            onClick={() => onChange(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  )
}
