import { Link } from 'react-router-dom'
import { Header } from '../components/layout/Header'

export default function NotFoundPage() {
  return (
    <>
      <Header
        title="404"
        subtitle="页面未找到"
      />
      <div className="container">
        <div className="empty-state">
          <div className="icon">🔍</div>
          <p>您访问的页面不存在</p>
          <Link to="/" className="watch-btn" style={{ maxWidth: 200, margin: '20px auto' }}>
            返回首页
          </Link>
        </div>
      </div>
    </>
  )
}
