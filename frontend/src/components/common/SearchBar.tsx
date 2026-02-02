import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { searchItems } from '../../services/api'
import type { Item } from '../../types'

const MODULE_NAMES: Record<string, string> = {
  youtube: 'YouTube',
  substack: 'Substack',
  twitter: 'X / Twitter',
  products: 'Product',
  business: '商业',
  apple_podcast: '播客',
}

export function SearchBar() {
  const [isOpen, setIsOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Item[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()

  // 键盘快捷键 Cmd+K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsOpen(true)
      }
      if (e.key === 'Escape') {
        setIsOpen(false)
        setQuery('')
        setResults([])
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [])

  // 打开时聚焦输入框
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  // 点击外部关闭
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false)
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isOpen])

  // 搜索
  useEffect(() => {
    if (!query.trim()) {
      setResults([])
      return
    }

    const timer = setTimeout(async () => {
      setIsLoading(true)
      try {
        const data = await searchItems(query)
        setResults(data.items)
      } catch (error) {
        console.error('Search failed:', error)
        setResults([])
      } finally {
        setIsLoading(false)
      }
    }, 300)

    return () => clearTimeout(timer)
  }, [query])

  const handleResultClick = (item: Item) => {
    setIsOpen(false)
    setQuery('')
    setResults([])
    // 跳转到对应模块页面，并传递选中的 item
    navigate(`/${item.module}`, { state: { selectedItem: item } })
  }

  return (
    <>
      {/* 搜索按钮 */}
      <button className="search-trigger" onClick={() => setIsOpen(true)}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>
        <span className="search-placeholder">搜索...</span>
        <span className="search-shortcut">⌘K</span>
      </button>

      {/* 搜索弹窗 */}
      {isOpen && (
        <div className="search-overlay">
          <div className="search-modal" ref={containerRef}>
            <div className="search-header">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              <input
                ref={inputRef}
                type="text"
                className="search-input"
                placeholder="搜索文章、项目、论文..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              {isLoading && <div className="search-spinner"></div>}
              <button className="search-close" onClick={() => setIsOpen(false)}>
                <span>ESC</span>
              </button>
            </div>

            <div className="search-results">
              {!query && (
                <div className="search-hint">
                  <p>输入关键词搜索站内内容</p>
                  <div className="search-tips">
                    <span>支持搜索：标题、摘要、来源</span>
                  </div>
                </div>
              )}

              {query && results.length === 0 && !isLoading && (
                <div className="search-empty">
                  <p>未找到相关内容</p>
                </div>
              )}

              {results.length > 0 && (
                <ul className="search-list">
                  {results.map((item) => (
                    <li key={item.id} className="search-item" onClick={() => handleResultClick(item)}>
                      <div className="search-item-icon">
                        {item.module === 'youtube' && '📺'}
                        {item.module === 'substack' && '📝'}
                        {item.module === 'twitter' && '𝕏'}
                        {item.module === 'products' && '🚀'}
                        {item.module === 'business' && '💼'}
                        {item.module === 'apple_podcast' && '🎧'}
                      </div>
                      <div className="search-item-content">
                        <div className="search-item-title">
                          {item.title_zh || item.title}
                        </div>
                        <div className="search-item-meta">
                          <span className="search-item-module">{MODULE_NAMES[item.module] || item.module}</span>
                          <span className="search-item-source">{item.source}</span>
                        </div>
                      </div>
                      <svg className="search-item-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M9 18l6-6-6-6"/>
                      </svg>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  )
}
