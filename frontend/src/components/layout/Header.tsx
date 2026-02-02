interface HeaderProps {
  title: string
  subtitle: string
  badge?: string
}

export function Header({ title, subtitle, badge }: HeaderProps) {
  const today = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return (
    <div className="header">
      {badge && <span className="header-badge">{badge}</span>}
      <h1>{title}</h1>
      <p>{today} · {subtitle}</p>
    </div>
  )
}
