import { useEffect } from 'react'
import type { Item } from '../../types'
import { Tags } from '../common/Tag'
import { DetailContext } from '../../App'

interface DetailPanelProps {
  item: Item | null
  onClose: () => void
}

function formatStars(stars: number): string {
  if (stars >= 1000) {
    return (stars / 1000).toFixed(1).replace(/\.0$/, '') + 'k'
  }
  return String(stars)
}

export function DetailPanel({ item, onClose }: DetailPanelProps) {
  const duration = item?.extra?.duration as string | undefined
  const videoId = item?.id?.startsWith('youtube_') ? item.id.replace('youtube_', '') : null
  const tweetId = item?.extra?.tweet_id as string || (item?.id?.startsWith('twitter_') ? item.id.replace('twitter_', '') : null)
  const guests = item?.extra?.guests as Array<{name: string, name_zh: string, title: string}> | undefined
  const topics = item?.extra?.topics as string[] | undefined
  const isPodcast = item?.id?.startsWith('youtube_') || item?.id?.startsWith('apple_podcast_')
  const isApplePodcast = item?.id?.startsWith('apple_podcast_')
  const audioUrl = item?.extra?.audio_url as string | undefined

  // Repo specific data
  const isRepo = item?.module === 'products'
  const repoPath = item?.extra?.repo_path as string | undefined
  const stars = (item?.extra?.stars as number) || 0
  const language = (item?.extra?.language as string) || ''
  const starsWeek = (item?.extra?.stars_week as string) || ''
  const forks = (item?.extra?.forks as string) || ''
  const owner = (item?.extra?.owner as string) || ''
  const features = (item?.extra?.features as string[]) || []
  const techStack = (item?.extra?.tech_stack as string[]) || []
  const ogImage = repoPath ? `https://opengraph.githubassets.com/1/${repoPath}` : ''

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

  // Repo detail panel
  if (isRepo) {
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
            {/* Repo Screenshot */}
            {ogImage && (
              <div className="detail-thumbnail">
                <img src={ogImage} alt={item.title} />
              </div>
            )}

            {/* Repo Header */}
            <div className="repo-detail-header">
              <span className="repo-owner">{owner}</span>
              <span className="repo-separator">/</span>
              <h2 className="detail-title" style={{ display: 'inline', margin: 0 }}>{item.title}</h2>
            </div>

            {/* Stats */}
            <div className="repo-hero-stats" style={{ marginTop: 'var(--space-md)' }}>
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

            {/* Description */}
            {item.summary && (
              <div className="detail-section">
                <div className="section-label">Description</div>
                <p className="section-text">{item.summary}</p>
              </div>
            )}

            {/* Features */}
            {features.length > 0 && (
              <div className="detail-section">
                <div className="section-label">Features</div>
                <ul className="detail-points">
                  {features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Tech Stack */}
            {techStack.length > 0 && (
              <div className="detail-section">
                <div className="section-label">Tech Stack</div>
                <div className="tech-tags">
                  {techStack.map((tech, index) => (
                    <span key={index} className="tech-tag">{tech}</span>
                  ))}
                </div>
              </div>
            )}

            {/* Tags */}
            {item.tags && item.tags.length > 0 && (
              <div className="detail-section">
                <div className="section-label">Tags</div>
                <Tags tags={item.tags} />
              </div>
            )}

            {/* Link Button */}
            <a
              href={item.link}
              target="_blank"
              rel="noopener noreferrer"
              className="repo-link-btn"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/>
              </svg>
              View on GitHub
            </a>
          </div>
        </div>
      </>
    )
  }

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
          {/* 播客专用：嘉宾信息 */}
          {isPodcast && guests && guests.length > 0 && (
            <div className="detail-section">
              <div className="section-label">做客嘉宾</div>
              <div className="guest-list">
                {guests.map((guest, index) => (
                  <div key={index} className="guest-item">
                    <div className="guest-name">
                      {guest.name_zh || guest.name}
                      {guest.name_zh && guest.name && guest.name_zh !== guest.name && (
                        <span className="guest-name-en"> ({guest.name})</span>
                      )}
                    </div>
                    {guest.title && <div className="guest-title">{guest.title}</div>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 播客专用：讨论主题 */}
          {isPodcast && topics && topics.length > 0 && (
            <div className="detail-section">
              <div className="section-label">讨论主题</div>
              <ul className="detail-points">
                {topics.map((topic, index) => (
                  <li key={index}>{topic}</li>
                ))}
              </ul>
            </div>
          )}

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

          {/* 原有卡片形态 */}
          <div className="detail-card">
            {/* YouTube 嵌入 */}
            {videoId && (
              <div className="detail-embed">
                <iframe
                  src={`https://www.youtube.com/embed/${videoId}`}
                  allowFullScreen
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                />
              </div>
            )}

            {/* Twitter 嵌入 */}
            {tweetId && !videoId && (
              <div className="detail-tweet">
                <blockquote className="twitter-tweet" data-theme="light">
                  <a href={`https://twitter.com/x/status/${tweetId}`}></a>
                </blockquote>
              </div>
            )}

            {/* Apple Podcast 音频播放器 */}
            {isApplePodcast && (
              <div className="detail-audio">
                {item.thumbnail && (
                  <div className="audio-cover">
                    <img src={item.thumbnail} alt={item.title} />
                  </div>
                )}
                {audioUrl && (
                  <audio controls className="audio-player">
                    <source src={audioUrl} type="audio/mpeg" />
                    Your browser does not support the audio element.
                  </audio>
                )}
                {duration && duration !== "N/A" && (
                  <div className="audio-duration">时长: {duration}</div>
                )}
              </div>
            )}

            {/* 缩略图（非视频/推文/播客时显示） */}
            {item.thumbnail && !videoId && !tweetId && !isApplePodcast && (
              <div className="detail-thumbnail">
                <img src={item.thumbnail} alt={item.title} />
                {duration && <span className="duration">{duration}</span>}
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
