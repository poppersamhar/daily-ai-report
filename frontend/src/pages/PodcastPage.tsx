import { useState } from 'react'
import { Header } from '../components/layout/Header'
import { useModuleDetail } from '../hooks/useModules'
import { DetailPanel } from '../components/cards/DetailPanel'
import type { Item } from '../types'
import '../styles/youtube.css'

type TabType = 'youtube' | 'apple_podcast'

export default function PodcastPage() {
  const [activeTab, setActiveTab] = useState<TabType>('youtube')
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  const { data: youtubeData, isLoading: youtubeLoading } = useModuleDetail('youtube')
  const { data: appleData, isLoading: appleLoading } = useModuleDetail('apple_podcast')

  const isLoading = activeTab === 'youtube' ? youtubeLoading : appleLoading
  const data = activeTab === 'youtube' ? youtubeData : appleData

  const allItems = data?.hero ? [data.hero, ...(data.items || [])] : (data?.items || [])

  return (
    <>
      <Header
        title="Podcast"
        subtitle={allItems.length > 0 ? `${allItems.length} ${activeTab === 'youtube' ? 'videos' : 'episodes'}` : 'AI Podcasts'}
        badge="Podcast"
      />

      {/* 子导航栏 */}
      <div className="sub-nav">
        <div className="sub-nav-inner">
          <button
            className={`sub-nav-btn${activeTab === 'youtube' ? ' active' : ''}`}
            onClick={() => setActiveTab('youtube')}
          >
            YouTube
          </button>
          <button
            className={`sub-nav-btn${activeTab === 'apple_podcast' ? ' active' : ''}`}
            onClick={() => setActiveTab('apple_podcast')}
          >
            Apple Podcast
          </button>
        </div>
      </div>

      <div className="youtube-container">
        {isLoading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading...</p>
          </div>
        ) : allItems.length === 0 ? (
          <div className="empty-state">
            <p>No content available</p>
          </div>
        ) : (
          <div className="video-grid">
            {allItems.map((item) => {
              if (activeTab === 'youtube') {
                const videoId = item.id.replace('youtube_', '')
                const duration = item.extra?.duration as string | undefined
                return (
                  <div key={item.id} className="video-card">
                    <button
                      className="video-detail-btn"
                      onClick={() => setSelectedItem(item)}
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
              } else {
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
              }
            })}
          </div>
        )}
      </div>

      <DetailPanel item={selectedItem} onClose={() => setSelectedItem(null)} />
    </>
  )
}
