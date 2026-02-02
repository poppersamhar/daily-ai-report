import { NavLink } from 'react-router-dom'
import { SearchBar } from '../common/SearchBar'

const navItems = [
  { path: '/', label: '首页' },
  { path: '/podcast', label: 'Podcast' },
  { path: '/twitter', label: 'Social' },
  { path: '/substack', label: 'News' },
  { path: '/products', label: 'Product' },
]

export function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-inner">
        <NavLink to="/" className="nav-brand">
          <img src="/logo.png" alt="Zerde" className="nav-logo" />
          Zerde
        </NavLink>
        <div className="nav-links">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `nav-link${isActive ? ' active' : ''}`
              }
            >
              {item.label}
            </NavLink>
          ))}
          <SearchBar />
        </div>
      </div>
    </nav>
  )
}
