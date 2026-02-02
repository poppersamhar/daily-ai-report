import { useState, useEffect } from 'react'
import { Header } from '../components/layout/Header'
import { useModuleDetail } from '../hooks/useModules'
import { TwitterDetailPanel } from '../components/cards/TwitterDetailPanel'
import type { Item } from '../types'
import '../styles/twitter.css'

export default function TwitterPage() {
  const { data, isLoading, error } = useModuleDetail('twitter')
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  const handleItemClick = (item: Item) => {
    setSelectedItem(item)
  }

  const handleCloseDetail = () => {
    setSelectedItem(null)
  }

  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://platform.twitter.com/widgets.js'
    script.async = true
    document.body.appendChild(script)

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script)
      }
    }
  }, [])

  useEffect(() => {
    if (data?.items || data?.hero) {
      // @ts-ignore
      if (window.twttr && window.twttr.widgets) {
        setTimeout(() => {
          // @ts-ignore
          window.twttr.widgets.load()
        }, 100)
      }
    }
  }, [data])

  if (isLoading) {
    return (
      <>
        <Header title="X / Twitter" subtitle="AI updates from X" badge="Social" />
        <div className="twitter-container">
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
        <Header title="X / Twitter" subtitle="AI updates from X" badge="Social" />
        <div className="twitter-container">
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
        title="X / Twitter"
        subtitle={hasItems ? `${allItems.length} tweets` : 'AI updates from X'}
        badge="Social"
      />
      <div className="twitter-container">
        {!hasItems ? (
          <div className="empty-state">
            <p>No tweets available</p>
          </div>
        ) : (
          <div className="masonry-container">
            {allItems.map((item) => {
              const tweetId = item.extra?.tweet_id as string || item.id.replace('twitter_', '')
              return (
                <div key={item.id} className="item">
                  <div className="tweet-card">
                    <button
                      className="tweet-detail-btn"
                      onClick={() => handleItemClick(item)}
                    >
                      Translation
                    </button>
                    <div className="twitter-embed">
                      <blockquote className="twitter-tweet" data-theme="light">
                        <a href={`https://twitter.com/x/status/${tweetId}`}></a>
                      </blockquote>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      <TwitterDetailPanel item={selectedItem} onClose={handleCloseDetail} />
    </>
  )
}
