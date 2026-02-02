import { useState } from 'react'
import { Header } from '../components/layout/Header'
import { useModuleDetail } from '../hooks/useModules'
import { DetailPanel } from '../components/cards/DetailPanel'
import type { Item } from '../types'
import '../styles/youtube.css'

export default function ApplePodcastPage() {
  const { data, isLoading, error } = useModuleDetail('apple_podcast')
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  if (isLoading) {
    return (
      <>
        <Header title="中文播客" subtitle="Chinese AI Podcasts" badge="Podcast" />
        <div className="youtube-container">
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading...</p>
          </div>
        </div>
      </>
    )
  }

  if (error) {
    return (
      <>
        <Header title="中文播客" subtitle="Chinese AI Podcasts" badge="Podcast" />
        <div className="youtube-container">
          <div className="empty-state">
            <p>Failed to load. Please try again.</p>
          </div>
        </div>
      </>
    )
  }

  const allItems = data?.hero ? [data.hero, ...(data.items || [])] : (data?.items || [])

  return (
    <>
      <Header
        title="中文播客"
        subtitle={allItems.length > 0 ? `${allItems.length} episodes` : 'Chinese AI Podcasts'}
        badge="Podcast"
      />
      <div className="youtube-container">
        {allItems.length === 0 ? (
          <div className="empty-state">
            <p>No podcasts available</p>
          </div>
        ) : (
          <div className="video-grid">
            {allItems.map((item) => {
              const duration = item.extra?.duration as string | undefined
              const audioUrl = item.extra?.audio_url as string | undefined
              return (
                <div key={item.id} className="video-card podcast-card">
                  <button
                    className="video-detail-btn"
                    onClick={() => setSelectedItem(item)}
                  >
                    Details
                  </button>
                  <div className="video-main">
                    {item.thumbnail ? (
                      <div className="podcast-cover">
                        <img src={item.thumbnail} alt={item.title} />
                        {audioUrl && (
                          <a href={audioUrl} target="_blank" rel="noopener noreferrer" className="play-btn">
                            ▶
                          </a>
                        )}
                      </div>
                    ) : (
                      <div className="podcast-cover podcast-cover-placeholder">
                        <span>🎧</span>
                        {audioUrl && (
                          <a href={audioUrl} target="_blank" rel="noopener noreferrer" className="play-btn">
                            ▶
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                  <div className="video-title-zh">
                    <p>{item.title_zh || item.title}</p>
                  </div>
                  {item.summary && (
                    <div className="video-summary">
                      <p>{item.summary}</p>
                    </div>
                  )}
                  <div className="video-info">
                    <span className="video-channel">{item.source}</span>
                    {duration && duration !== "N/A" && (
                      <span className="video-duration">{duration}</span>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
      <DetailPanel item={selectedItem} onClose={() => setSelectedItem(null)} />
    </>
  )
}
