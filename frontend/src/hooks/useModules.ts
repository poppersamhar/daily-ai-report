import { useQuery } from '@tanstack/react-query'
import { fetchModules, fetchModuleDetail, fetchWeeklySummary } from '../services/api'

export function useModules() {
  return useQuery({
    queryKey: ['modules'],
    queryFn: fetchModules,
  })
}

export function useModuleDetail(module: string, days: number = 7) {
  return useQuery({
    queryKey: ['module', module, days],
    queryFn: () => fetchModuleDetail(module, days),
    enabled: !!module,
  })
}

export function useWeeklySummary() {
  return useQuery({
    queryKey: ['weekly-summary'],
    queryFn: fetchWeeklySummary,
  })
}
