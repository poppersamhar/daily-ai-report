import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { Header } from '../components/layout/Header'
import { useModuleDetail } from '../hooks/useModules'
import { RepoCard, RepoHeroCard } from '../components/cards/RepoCard'
import { ProductHuntCard } from '../components/cards/ProductHuntCard'
import { DetailPanel } from '../components/cards/DetailPanel'
import { DateFilter } from '../components/common/DateFilter'
import type { Item } from '../types'

type TabType = 'github' | 'producthunt'

// 模拟 Product Hunt 数据（后续可替换为真实 API）
const MOCK_PRODUCTHUNT_DATA: Item[] = [
  {
    id: 'ph_1',
    module: 'producthunt',
    title: 'Cursor',
    title_zh: 'Cursor - AI 代码编辑器',
    summary: 'The AI-first code editor. Build software faster with AI that understands your codebase.',
    link: 'https://www.cursor.com',
    source: 'Product Hunt',
    author: 'Cursor Team',
    pub_date: new Date().toISOString(),
    thumbnail: 'https://ph-files.imgix.net/cursor-logo.png',
    tags: [
      { label: 'AI', type: 'topic' },
      { label: 'Developer Tools', type: 'topic' },
      { label: 'Productivity', type: 'topic' },
    ],
    fame_score: 1200,
    extra: {
      upvotes: 2847,
      comments: 342,
      tagline: 'The AI-first code editor',
      topics: ['Artificial Intelligence', 'Developer Tools', 'Productivity'],
    },
    core_insight: '',
    key_points: [],
    is_hero: 1,
  },
  {
    id: 'ph_2',
    module: 'producthunt',
    title: 'v0 by Vercel',
    title_zh: 'v0 - AI 生成 UI 组件',
    summary: 'Generate UI with simple text prompts. Copy, paste, ship.',
    link: 'https://v0.dev',
    source: 'Product Hunt',
    author: 'Vercel',
    pub_date: new Date().toISOString(),
    thumbnail: '',
    tags: [
      { label: 'AI', type: 'topic' },
      { label: 'Design Tools', type: 'topic' },
    ],
    fame_score: 980,
    extra: {
      upvotes: 1923,
      comments: 187,
      tagline: 'Generate UI with simple text prompts',
      topics: ['Artificial Intelligence', 'Design Tools', 'No-Code'],
    },
    core_insight: '',
    key_points: [],
    is_hero: 0,
  },
  {
    id: 'ph_3',
    module: 'producthunt',
    title: 'Perplexity',
    title_zh: 'Perplexity - AI 搜索引擎',
    summary: 'Ask anything. Get instant answers with cited sources.',
    link: 'https://perplexity.ai',
    source: 'Product Hunt',
    author: 'Perplexity AI',
    pub_date: new Date().toISOString(),
    thumbnail: '',
    tags: [
      { label: 'AI', type: 'topic' },
      { label: 'Search', type: 'topic' },
    ],
    fame_score: 890,
    extra: {
      upvotes: 1654,
      comments: 156,
      tagline: 'Ask anything. Get instant answers.',
      topics: ['Artificial Intelligence', 'Search Engine', 'Productivity'],
    },
    core_insight: '',
    key_points: [],
    is_hero: 0,
  },
  {
    id: 'ph_4',
    module: 'producthunt',
    title: 'Bolt.new',
    title_zh: 'Bolt.new - AI 全栈开发',
    summary: 'Prompt, run, edit, and deploy full-stack web apps.',
    link: 'https://bolt.new',
    source: 'Product Hunt',
    author: 'StackBlitz',
    pub_date: new Date().toISOString(),
    thumbnail: '',
    tags: [
      { label: 'AI', type: 'topic' },
      { label: 'Developer Tools', type: 'topic' },
    ],
    fame_score: 850,
    extra: {
      upvotes: 1432,
      comments: 198,
      tagline: 'Prompt, run, edit, and deploy full-stack web apps',
      topics: ['Artificial Intelligence', 'Developer Tools', 'Web Development'],
    },
    core_insight: '',
    key_points: [],
    is_hero: 0,
  },
  {
    id: 'ph_5',
    module: 'producthunt',
    title: 'Lovable',
    title_zh: 'Lovable - AI 应用构建器',
    summary: 'Build apps with AI. From idea to production in minutes.',
    link: 'https://lovable.dev',
    source: 'Product Hunt',
    author: 'Lovable',
    pub_date: new Date().toISOString(),
    thumbnail: '',
    tags: [
      { label: 'AI', type: 'topic' },
      { label: 'No-Code', type: 'topic' },
    ],
    fame_score: 780,
    extra: {
      upvotes: 1287,
      comments: 143,
      tagline: 'Build apps with AI',
      topics: ['Artificial Intelligence', 'No-Code', 'Productivity'],
    },
    core_insight: '',
    key_points: [],
    is_hero: 0,
  },
  {
    id: 'ph_6',
    module: 'producthunt',
    title: 'Replit Agent',
    title_zh: 'Replit Agent - AI 编程助手',
    summary: 'Build apps by describing what you want. AI handles the rest.',
    link: 'https://replit.com',
    source: 'Product Hunt',
    author: 'Replit',
    pub_date: new Date().toISOString(),
    thumbnail: '',
    tags: [
      { label: 'AI', type: 'topic' },
      { label: 'Developer Tools', type: 'topic' },
    ],
    fame_score: 720,
    extra: {
      upvotes: 1156,
      comments: 132,
      tagline: 'Build apps by describing what you want',
      topics: ['Artificial Intelligence', 'Developer Tools', 'IDE'],
    },
    core_insight: '',
    key_points: [],
    is_hero: 0,
  },
]

export default function ProductPage() {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState<TabType>('github')
  const [days, setDays] = useState(7)
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  // GitHub Trending 数据
  const { data: githubData, isLoading: githubLoading } = useModuleDetail('products', days)

  // Product Hunt 数据（目前使用模拟数据）
  const productHuntData = MOCK_PRODUCTHUNT_DATA
  const productHuntLoading = false

  // 从搜索跳转过来时，自动打开详情面板
  useEffect(() => {
    const state = location.state as { selectedItem?: Item } | null
    if (state?.selectedItem) {
      setSelectedItem(state.selectedItem)
      window.history.replaceState({}, document.title)
    }
  }, [location.state])

  const handleItemClick = (item: Item) => {
    setSelectedItem(item)
  }

  const handleCloseDetail = () => {
    setSelectedItem(null)
  }

  const totalCount = activeTab === 'github'
    ? (githubData?.total || 0)
    : productHuntData.length

  return (
    <>
      <Header
        title="Product"
        subtitle={totalCount > 0 ? `${totalCount} products` : 'AI Products & Tools'}
        badge="Product"
      />

      {/* 子导航栏 */}
      <div className="sub-nav">
        <div className="sub-nav-inner">
          <button
            className={`sub-nav-btn${activeTab === 'github' ? ' active' : ''}`}
            onClick={() => setActiveTab('github')}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style={{ marginRight: '6px' }}>
              <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/>
            </svg>
            GitHub Trending
            <span className="sub-nav-count">{githubData?.total || 0}</span>
          </button>
          <button
            className={`sub-nav-btn${activeTab === 'producthunt' ? ' active' : ''}`}
            onClick={() => setActiveTab('producthunt')}
          >
            <svg width="16" height="16" viewBox="0 0 40 40" fill="currentColor" style={{ marginRight: '6px' }}>
              <path d="M20 0C8.954 0 0 8.954 0 20s8.954 20 20 20 20-8.954 20-20S31.046 0 20 0zm0 36c-8.837 0-16-7.163-16-16S11.163 4 20 4s16 7.163 16 16-7.163 16-16 16zm-2-26h-6v20h4v-6h2c4.418 0 8-3.582 8-8s-3.582-6-8-6zm0 10h-2v-6h2c2.21 0 4 1.79 4 3s-1.79 3-4 3z"/>
            </svg>
            Product Hunt
            <span className="sub-nav-count">{productHuntData.length}</span>
          </button>
        </div>
      </div>

      <div className="container product-container">
        {/* GitHub Tab */}
        {activeTab === 'github' && (
          <>
            <DateFilter value={days} onChange={setDays} />

            {githubLoading ? (
              <div className="loading">
                <div className="loading-spinner"></div>
                <p>Loading...</p>
              </div>
            ) : (
              <>
                {githubData?.hero && (
                  <section className="product-section">
                    <div className="section-header">
                      <h2 className="section-title">Featured</h2>
                      <span className="section-badge">Trending</span>
                    </div>
                    <RepoHeroCard item={githubData.hero} onClick={handleItemClick} />
                  </section>
                )}

                {githubData?.items && githubData.items.length > 0 && (
                  <section className="product-section">
                    <div className="section-header">
                      <h2 className="section-title">Trending Repos</h2>
                      <span className="section-count">{githubData.items.length} repos</span>
                    </div>
                    <div className="product-grid">
                      {githubData.items.map((item) => (
                        <RepoCard key={item.id} item={item} onClick={handleItemClick} />
                      ))}
                    </div>
                  </section>
                )}

                {!githubData?.hero && (!githubData?.items || githubData.items.length === 0) && (
                  <div className="empty-state">
                    <div className="empty-icon">🚀</div>
                    <p>No trending repos available</p>
                  </div>
                )}
              </>
            )}
          </>
        )}

        {/* Product Hunt Tab */}
        {activeTab === 'producthunt' && (
          <>
            {productHuntLoading ? (
              <div className="loading">
                <div className="loading-spinner"></div>
                <p>Loading...</p>
              </div>
            ) : (
              <>
                <section className="product-section">
                  <div className="section-header">
                    <h2 className="section-title">Weekly Top Products</h2>
                    <span className="section-badge ph-badge">Product Hunt</span>
                  </div>
                  <div className="ph-grid">
                    {productHuntData.map((item, index) => (
                      <ProductHuntCard
                        key={item.id}
                        item={item}
                        rank={index + 1}
                        onClick={handleItemClick}
                      />
                    ))}
                  </div>
                </section>
              </>
            )}
          </>
        )}
      </div>

      <DetailPanel item={selectedItem} onClose={handleCloseDetail} />
    </>
  )
}
