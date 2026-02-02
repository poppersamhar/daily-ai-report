import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { Header } from '../components/layout/Header'
import { useModuleDetail } from '../hooks/useModules'
import { TwitterDetailPanel } from '../components/cards/TwitterDetailPanel'
import { CompactCard } from '../components/cards/CompactCard'
import { DetailPanel } from '../components/cards/DetailPanel'
import type { Item } from '../types'
import '../styles/twitter.css'

type TabType = 'twitter' | 'reddit'

export default function SocialPage() {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState<TabType>('twitter')
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  const { data: twitterData, isLoading: twitterLoading } = useModuleDetail('twitter')
  const { data: redditData, isLoading: redditLoading } = useModuleDetail('reddit')

  const isLoading = activeTab === 'twitter' ? twitterLoading : redditLoading
  const data = activeTab === 'twitter' ? twitterData : redditData

  const allItems = data?.hero ? [data.hero, ...(data.items || [])] : (data?.items || [])

  // 从搜索跳转过来时，自动打开详情面板
  useEffect(() => {
    const state = location.state as { selectedItem?: Item } | null
    if (state?.selectedItem) {
      setSelectedItem(state.selectedItem)
      window.history.replaceState({}, document.title)
    }
  }, [location.state])

  // 加载 Twitter widgets
  useEffect(() => {
    if (activeTab === 'twitter') {
      const script = document.createElement('script')
      script.src = 'https://platform.twitter.com/widgets.js'
      script.async = true
      document.body.appendChild(script)

      return () => {
        if (document.body.contains(script)) {
          document.body.removeChild(script)
        }
      }
    }
  }, [activeTab])

  useEffect(() => {
    if (activeTab === 'twitter' && (data?.items || data?.hero)) {
      // @ts-ignore
      if (window.twttr && window.twttr.widgets) {
        setTimeout(() => {
          // @ts-ignore
          window.twttr.widgets.load()
        }, 100)
      }
    }
  }, [data, activeTab])

  const handleItemClick = (item: Item) => {
    setSelectedItem(item)
  }

  const handleCloseDetail = () => {
    setSelectedItem(null)
  }

  return (
    <>
      <Header
        title="Social"
        subtitle={allItems.length > 0 ? `${allItems.length} posts` : 'AI Social Media'}
        badge="Social"
      />

      {/* 子导航栏 */}
      <div className="sub-nav">
        <div className="sub-nav-inner">
          <button
            className={`sub-nav-btn${activeTab === 'twitter' ? ' active' : ''}`}
            onClick={() => setActiveTab('twitter')}
          >
            X / Twitter
          </button>
          <button
            className={`sub-nav-btn${activeTab === 'reddit' ? ' active' : ''}`}
            onClick={() => setActiveTab('reddit')}
          >
            Reddit
          </button>
        </div>
      </div>

      {activeTab === 'twitter' ? (
        <div className="twitter-container">
          {isLoading ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>Loading...</p>
            </div>
          ) : allItems.length === 0 ? (
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
      ) : (
        <div className="container">
          {isLoading ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>Loading...</p>
            </div>
          ) : allItems.length === 0 ? (
            <div className="empty-state">
              <p>Reddit 数据即将上线</p>
            </div>
          ) : (
            <div className="social-list">
              {allItems.map((item) => (
                <CompactCard key={item.id} item={item} onClick={handleItemClick} />
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'twitter' ? (
        <TwitterDetailPanel item={selectedItem} onClose={handleCloseDetail} />
      ) : (
        <DetailPanel item={selectedItem} onClose={handleCloseDetail} />
      )}
    </>
  )
}
