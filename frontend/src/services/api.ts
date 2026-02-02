import axios from 'axios'
import type { ModulesResponse, ModuleDetailResponse, WeeklySummaryResponse, ItemListResponse } from '../types'

const API_URL = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  timeout: 30000,
})

export async function fetchModules(): Promise<ModulesResponse> {
  const { data } = await api.get<ModulesResponse>('/modules/')
  return data
}

export async function fetchModuleDetail(module: string, days: number = 7): Promise<ModuleDetailResponse> {
  const { data } = await api.get<ModuleDetailResponse>(`/modules/${module}`, {
    params: { days }
  })
  return data
}

export async function fetchWeeklySummary(): Promise<WeeklySummaryResponse> {
  const { data } = await api.get<WeeklySummaryResponse>('/weekly/summary')
  return data
}

export async function searchItems(q: string, module?: string): Promise<ItemListResponse> {
  const { data } = await api.get<ItemListResponse>('/items/', {
    params: { q, module, page_size: 10 }
  })
  return data
}

export default api
