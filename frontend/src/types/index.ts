export interface Tag {
  label: string
  type: 'company' | 'person' | 'topic' | 'tech' | 'event' | 'lang'
}

export interface Item {
  id: string
  module: string
  title: string
  title_zh: string
  summary: string
  link: string
  source: string
  author: string
  pub_date: string
  thumbnail: string
  tags: Tag[]
  fame_score: number
  extra: Record<string, unknown>
  core_insight: string
  key_points: string[]
  is_hero: number
}

export interface ItemListResponse {
  items: Item[]
  total: number
  page: number
  page_size: number
}

export interface ModuleInfo {
  module: string
  module_zh: string
  icon: string
  hero: Item | null
  items: Item[]
  total: number
}

export interface ModulesResponse {
  date: string
  modules: ModuleInfo[]
}

export interface ModuleDetailResponse {
  module: string
  module_zh: string
  icon: string
  hero: Item | null
  items: Item[]
  total: number
}

export interface HotTopic {
  topic: string
  description: string
  trend: '上升' | '下降' | '持平'
}

export interface KeyEvent {
  title: string
  summary: string
}

export interface WeeklySummary {
  id: string
  week_start: string
  week_end: string
  headline: string
  hot_topics: HotTopic[]
  trend_analysis: string
  key_events: KeyEvent[]
  company_mentions: Record<string, number>
  total_items: number
  modules_stats: Record<string, { count: number; top_items: string[] }>
  created_at: string
}

export interface WeeklySummaryResponse {
  data: WeeklySummary | null
  error?: string
}
