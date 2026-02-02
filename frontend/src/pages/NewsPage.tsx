import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { Header } from '../components/layout/Header'
import { useModuleDetail } from '../hooks/useModules'
import { SubstackCard, SubstackHeroCard } from '../components/cards/SubstackCard'
import { DetailPanel } from '../components/cards/DetailPanel'
import type { Item } from '../types'

type TabType = 'blog' | 'newsletter'

export default function NewsPage() {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState<TabType>('blog')
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  const { data, isLoading } = useModuleDetail('substack')

  // 根据 extra.type 过滤数据
  const blogItems = (data?.items || []).filter(item => item.extra?.type === 'official')
  const newsletterItems = (data?.items || []).filter(item => item.extra?.type === 'substack')

  // 获取 hero（优先从对应类型中选择）
  const blogHero = data?.hero?.extra?.type === 'official' ? data.hero : blogItems[0] || null
  const newsletterHero = data?.hero?.extra?.type === 'substack' ? data.hero : newsletterItems[0] || null

  // 当前显示的数据
  const currentHero = activeTab === 'blog' ? blogHero : newsletterHero
  const currentItems = activeTab === 'blog'
    ? blogItems.filter(item => item.id !== blogHero?.id)
    : newsletterItems.filter(item => item.id !== newsletterHero?.id)

  // 从搜索跳转过来时，自动打开详情面板
  useEffect(() => {
    const state = location.state as { selectedItem?: Item } | null
    if (state?.selectedItem) {
      setSelectedItem(state.selectedItem)
      // 根据 item 类型切换 tab
      if (state.selectedItem.extra?.type === 'official') {
        setActiveTab('blog')
      } else {
        setActiveTab('newsletter')
      }
      window.history.replaceState({}, document.title)
    }
  }, [location.state])

  const handleItemClick = (item: Item) => {
    setSelectedItem(item)
  }

  const handleCloseDetail = () => {
    setSelectedItem(null)
  }

  const totalCount = activeTab === 'blog' ? blogItems.length : newsletterItems.length

  return (
    <>
      <Header
        title="News"
        subtitle={totalCount > 0 ? `${totalCount} articles` : 'AI News & Blogs'}
        badge="News"
      />

      {/* 子导航栏 */}
      <div className="sub-nav">
        <div className="sub-nav-inner">
          <button
            className={`sub-nav-btn${activeTab === 'blog' ? ' active' : ''}`}
            onClick={() => setActiveTab('blog')}
          >
            Official Blog
            <span className="sub-nav-count">{blogItems.length}</span>
          </button>
          <button
            className={`sub-nav-btn${activeTab === 'newsletter' ? ' active' : ''}`}
            onClick={() => setActiveTab('newsletter')}
          >
            Newsletter
            <span className="sub-nav-count">{newsletterItems.length}</span>
          </button>
        </div>
      </div>

      <div className="container news-container">
        {isLoading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading...</p>
          </div>
        ) : (
          <>
            {/* Featured Hero */}
            {currentHero && (
              <section className="news-section">
                <div className="section-header">
                  <h2 className="section-title">Featured</h2>
                  <span className="section-badge">Top Story</span>
                </div>
                <SubstackHeroCard item={currentHero} onClick={handleItemClick} />
              </section>
            )}

            {/* News Grid */}
            {currentItems.length > 0 && (
              <section className="news-section">
                <div className="section-header">
                  <h2 className="section-title">Latest</h2>
                  <span className="section-count">{currentItems.length} articles</span>
                </div>
                <div className="news-grid">
                  {currentItems.map((item) => (
                    <SubstackCard key={item.id} item={item} onClick={handleItemClick} />
                  ))}
                </div>
              </section>
            )}

            {!currentHero && currentItems.length === 0 && (
              <div className="empty-state">
                <div className="empty-icon">📰</div>
                <p>No content available</p>
              </div>
            )}
          </>
        )}
      </div>

      <DetailPanel item={selectedItem} onClose={handleCloseDetail} />
    </>
  )
}
