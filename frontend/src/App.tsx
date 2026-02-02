import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Navbar } from './components/layout/Navbar'
import { Footer } from './components/layout/Footer'
import HomePage from './pages/HomePage'
import ModulePage from './pages/ModulePage'
import SocialPage from './pages/SocialPage'
import NewsPage from './pages/NewsPage'
import PodcastPage from './pages/PodcastPage'
import ProductPage from './pages/ProductPage'
import NotFoundPage from './pages/NotFoundPage'

// 创建一个全局状态来控制详情面板
export const DetailContext = {
  setOpen: (open: boolean) => {
    const app = document.querySelector('.app')
    if (app) {
      if (open) {
        app.classList.add('detail-open')
      } else {
        app.classList.remove('detail-open')
      }
    }
  }
}

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/twitter" element={<SocialPage />} />
            <Route path="/substack" element={<NewsPage />} />
            <Route path="/podcast" element={<PodcastPage />} />
            <Route path="/products" element={<ProductPage />} />
            <Route path="/:module" element={<ModulePage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App
