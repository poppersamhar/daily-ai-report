import { useState } from 'react'
import { Header } from '../components/layout/Header'
import { useModuleDetail } from '../hooks/useModules'
import { DetailPanel } from '../components/cards/DetailPanel'
import type { Item } from '../types'
import '../styles/youtube.css'

export default function YouTubePage() {
  const { data, isLoading, error } = useModuleDetail('youtube')
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  const handleItemClick = (item: Item) => {
    setSelectedItem(item)
  }

  const handleCloseDetail = () => {
    setSelectedItem(null)
  }

  if (isLoading) {
    return (
      <>
        <Header title="Podcast" subtitle="AI video content" badge="Podcast" />
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
        <Header title="Podcast" subtitle="AI video content" badge="Podcast" />
        <div className="youtube-container">
          <div className="empty-state">
            <p>Failed to load. Please try again.</p>
          </div>
        </div>
      </>
    )
  }

  const allItems = data?.hero ? [data.hero, ...(data.items || [])] : (data?.items || [])
  const hasItems = allItems.length > 0

  return (
    <>
      <Header
        title="Podcast"
        subtitle={hasItems ? `${allItems.length} videos` : 'AI video content'}
        badge="Podcast"
      />
      <div className="youtube-container">
        {!hasItems ? (
          <div className="empty-state">
            <p>No videos available</p>
          </div>
        ) : (
          <div className="video-grid">
            {allItems.map((item) => {
              const videoId = item.id.replace('youtube_', '')
              const duration = item.extra?.duration as string | undefined
              return (
                <div key={item.id} className="video-card">
                  <button
                    className="video-detail-btn"
                    onClick={() => handleItemClick(item)}
                  >
                    Details
                  </button>
                  <div className="video-main">
                    <div className="video-embed">
                      <iframe
                        src={`https://www.youtube.com/embed/${videoId}`}
                        allowFullScreen
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      ></iframe>
                    </div>
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
                    {duration && (
                      <span className="video-duration">{duration}</span>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      <DetailPanel item={selectedItem} onClose={handleCloseDetail} />
    </>
  )
}
