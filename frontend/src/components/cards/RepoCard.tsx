import type { Item } from '../../types'

interface RepoCardProps {
  item: Item
  onClick?: (item: Item) => void
}

function formatStars(stars: number): string {
  if (stars >= 1000) {
    return (stars / 1000).toFixed(1).replace(/\.0$/, '') + 'k'
  }
  return String(stars)
}

export function RepoCard({ item, onClick }: RepoCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  const stars = (item.extra?.stars as number) || 0
  const language = (item.extra?.language as string) || ''
  const starsWeek = (item.extra?.stars_week as string) || ''
  const forks = (item.extra?.forks as string) || ''
  const owner = (item.extra?.owner as string) || ''
  const repoPath = (item.extra?.repo_path as string) || ''

  // GitHub opengraph image for repo screenshot
  const ogImage = repoPath
    ? `https://opengraph.githubassets.com/1/${repoPath}`
    : ''

  return (
    <div className="repo-card" onClick={handleClick}>
      {ogImage && (
        <div className="repo-screenshot">
          <img src={ogImage} alt={item.title} loading="lazy" />
        </div>
      )}

      <div className="repo-content">
        <div className="repo-header">
          <span className="repo-owner">{owner}</span>
          <span className="repo-separator">/</span>
          <h3 className="repo-name">{item.title}</h3>
        </div>

        {item.summary && (
          <p className="repo-description">{item.summary}</p>
        )}

        <div className="repo-meta">
          {language && (
            <span className="repo-language">
              <span className={`lang-dot lang-${language.toLowerCase()}`}></span>
              {language}
            </span>
          )}

          <span className="repo-stars">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25z"/>
            </svg>
            {formatStars(stars)}
          </span>

          {forks && (
            <span className="repo-forks">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"/>
              </svg>
              {forks}
            </span>
          )}

          {starsWeek && (
            <span className="repo-trending">
              <svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8.75 1.75V5H12a.75.75 0 0 1 .53 1.28l-7.5 7.5a.75.75 0 0 1-1.28-.53V9.75H1a.75.75 0 0 1-.53-1.28l7.5-7.5a.75.75 0 0 1 1.28.53Z"/>
              </svg>
              {starsWeek}
            </span>
          )}
        </div>

        {item.tags && item.tags.length > 0 && (
          <div className="repo-tags">
            {item.tags.map((tag, index) => (
              <span key={index} className={`repo-tag tag-${tag.type}`}>
                {tag.label}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export function RepoHeroCard({ item, onClick }: RepoCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onClick?.(item)
  }

  const stars = (item.extra?.stars as number) || 0
  const language = (item.extra?.language as string) || ''
  const starsWeek = (item.extra?.stars_week as string) || ''
  const forks = (item.extra?.forks as string) || ''
  const owner = (item.extra?.owner as string) || ''
  const repoPath = (item.extra?.repo_path as string) || ''
  const features = (item.extra?.features as string[]) || []
  const techStack = (item.extra?.tech_stack as string[]) || []

  const ogImage = repoPath
    ? `https://opengraph.githubassets.com/1/${repoPath}`
    : ''

  return (
    <div className="repo-hero-card" onClick={handleClick}>
      {ogImage && (
        <div className="repo-hero-screenshot">
          <img src={ogImage} alt={item.title} loading="lazy" />
          <span className="repo-hero-badge">Featured</span>
        </div>
      )}

      <div className="repo-hero-content">
        <div className="repo-hero-header">
          <span className="repo-owner">{owner}</span>
          <span className="repo-separator">/</span>
          <h2 className="repo-hero-name">{item.title}</h2>
        </div>

        {item.summary && (
          <p className="repo-hero-description">{item.summary}</p>
        )}

        <div className="repo-hero-stats">
          {language && (
            <span className="repo-stat">
              <span className={`lang-dot lang-${language.toLowerCase()}`}></span>
              {language}
            </span>
          )}

          <span className="repo-stat">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25z"/>
            </svg>
            <strong>{formatStars(stars)}</strong> stars
          </span>

          {forks && (
            <span className="repo-stat">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"/>
              </svg>
              <strong>{forks}</strong> forks
            </span>
          )}

          {starsWeek && (
            <span className="repo-stat trending">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8.75 1.75V5H12a.75.75 0 0 1 .53 1.28l-7.5 7.5a.75.75 0 0 1-1.28-.53V9.75H1a.75.75 0 0 1-.53-1.28l7.5-7.5a.75.75 0 0 1 1.28.53Z"/>
              </svg>
              {starsWeek}
            </span>
          )}
        </div>

        {item.tags && item.tags.length > 0 && (
          <div className="repo-tags">
            {item.tags.map((tag, index) => (
              <span key={index} className={`repo-tag tag-${tag.type}`}>
                {tag.label}
              </span>
            ))}
          </div>
        )}

        {features.length > 0 && (
          <div className="repo-features">
            <h4>Features</h4>
            <ul>
              {features.slice(0, 4).map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
          </div>
        )}

        {techStack.length > 0 && (
          <div className="repo-tech-stack">
            <h4>Tech Stack</h4>
            <div className="tech-tags">
              {techStack.map((tech, index) => (
                <span key={index} className="tech-tag">{tech}</span>
              ))}
            </div>
          </div>
        )}

        <a
          href={item.link}
          target="_blank"
          rel="noopener noreferrer"
          className="repo-link-btn"
          onClick={(e) => e.stopPropagation()}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/>
          </svg>
          View on GitHub
        </a>
      </div>
    </div>
  )
}
