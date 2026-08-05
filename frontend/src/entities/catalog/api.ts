import { apiClient } from '../../shared/api/client';
import type { MenuCategory, MenuItem } from './types';

export interface MenuQuery {
  categoryId?: string;
  search?: string;
  limit?: number;
  offset?: number;
  signal?: AbortSignal;
}

export const catalogApi = {
  getCategories(): Promise<MenuCategory[]> {
    return apiClient.get<MenuCategory[]>('/api/v1/catalog/categories?limit=100&offset=0');
  },
  getMenuItems(query: MenuQuery = {}): Promise<MenuItem[]> {
    const params = new URLSearchParams({
      limit: String(query.limit ?? 24),
      offset: String(query.offset ?? 0),
    });
    if (query.categoryId) params.set('category_id', query.categoryId);
    if (query.search?.trim()) params.set('search', query.search.trim());
    return apiClient.get<MenuItem[]>(`/api/v1/catalog/menu-items?${params}`, query.signal);
  },
  getById(id: string): Promise<MenuItem> {
    return apiClient.get<MenuItem>(`/api/v1/catalog/menu-items/${id}`);
  },
};
