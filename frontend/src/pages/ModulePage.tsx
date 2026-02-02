import { useState, useEffect } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { useModuleDetail } from '../hooks/useModules'
import { Header } from '../components/layout/Header'
import { HeroCard } from '../components/cards/HeroCard'
import { ItemCard } from '../components/cards/ItemCard'
import { CompactCard } from '../components/cards/CompactCard'
import { RepoCard, RepoHeroCard } from '../components/cards/RepoCard'
import { SubstackCard, SubstackHeroCard } from '../components/cards/SubstackCard'
import { DetailPanel } from '../components/cards/DetailPanel'
import { DateFilter } from '../components/common/DateFilter'
import type { Item } from '../types'

const MODULE_CONFIG: Record<string, { title: string; badge: string; showThumbnail: boolean; isRepo?: boolean; isSubstack?: boolean }> = {
  youtube: { title: 'YouTube', badge: 'Video', showThumbnail: true },
  twitter: { title: 'X / Twitter', badge: 'Social', showThumbnail: false },
  substack: { title: 'News', badge: 'Newsletter', showThumbnail: false, isSubstack: true },
  products: { title: 'Product', badge: 'GitHub', showThumbnail: false, isRepo: true },
  business: { title: 'Business', badge: 'News', showThumbnail: false },
  apple_podcast: { title: '中文播客', badge: 'Podcast', showThumbnail: false },
}

export default function ModulePage() {
  const { module } = useParams<{ module: string }>()
  const location = useLocation()
  const [days, setDays] = useState(7)
  const { data, isLoading, error } = useModuleDetail(module || '', days)
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  // 从搜索跳转过来时，自动打开详情面板
  useEffect(() => {
    const state = location.state as { selectedItem?: Item } | null
    if (state?.selectedItem) {
      setSelectedItem(state.selectedItem)
      // 清除 state，避免刷新页面时重复打开
      window.history.replaceState({}, document.title)
    }
  }, [location.state])

  const handleItemClick = (item: Item) => {
    setSelectedItem(item)
  }

  const handleCloseDetail = () => {
    setSelectedItem(null)
  }

  const config = MODULE_CONFIG[module || ''] || { title: module || '', badge: '', showThumbnail: false }

  if (isLoading) {
    return (
      <>
        <Header
          title={config.title}
          subtitle="Loading..."
          badge={config.badge}
        />
        <div className="container">
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading...</p>
          </div>
        </div>
      </>
    )
  }

  if (error || !data) {
    return (
      <>
        <Header
          title={config.title}
          subtitle="Error"
          badge={config.badge}
        />
        <div className="container">
          <div className="empty-state">
            <p>Failed to load. Please try again.</p>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <Header
        title={data.module_zh || config.title}
        subtitle={`${data.total} items`}
        badge={config.badge}
      />
      <div className="container">
        <DateFilter value={days} onChange={setDays} />

        {data.hero && (
          <>
            <h2 className="section-title">Featured</h2>
            {config.isRepo ? (
              <RepoHeroCard item={data.hero} onClick={handleItemClick} />
            ) : config.isSubstack ? (
              <SubstackHeroCard item={data.hero} onClick={handleItemClick} />
            ) : (
              <HeroCard
                item={data.hero}
                moduleIcon={data.icon}
              />
            )}
          </>
        )}

        {data.items.length > 0 && (
          <>
            <h2 className="section-title">More</h2>
            {config.isRepo
              ? data.items.map((item) => (
                  <RepoCard key={item.id} item={item} onClick={handleItemClick} />
                ))
              : config.isSubstack
              ? data.items.map((item) => (
                  <SubstackCard key={item.id} item={item} onClick={handleItemClick} />
                ))
              : config.showThumbnail
              ? data.items.map((item) => (
                  <ItemCard key={item.id} item={item} showThumbnail onClick={handleItemClick} />
                ))
              : data.items.map((item) => (
                  <CompactCard key={item.id} item={item} onClick={handleItemClick} />
                ))}
          </>
        )}

        {!data.hero && data.items.length === 0 && (
          <div className="empty-state">
            <p>No content available</p>
          </div>
        )}
      </div>

      <DetailPanel item={selectedItem} onClose={handleCloseDetail} />
    </>
  )
}
