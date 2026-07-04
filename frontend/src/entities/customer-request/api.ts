import type { CustomerRequest, CustomerRequestStatus } from './model';
import { mockCustomerRequests } from './mockData';
import { apiClient } from '../../shared/api/client';
import { config } from '../../shared/config/env';

// ============================================
// API для работы с заявками
// Поддерживает mock и реальный backend
// ============================================

// Mock реализация
let mockRequests = [...mockCustomerRequests];

const mockApi = {
  async getAdminRequests(): Promise<CustomerRequest[]> {
    await new Promise((resolve) => setTimeout(resolve, 600));
    return mockRequests;
  },

  async updateRequestStatus(
    id: string,
    status: CustomerRequestStatus
  ): Promise<CustomerRequest> {
    await new Promise((resolve) => setTimeout(resolve, 400));
    const index = mockRequests.findIndex((r) => r.id === id);
    if (index === -1) {
      throw new Error('Заявка не найдена');
    }
    mockRequests[index] = { ...mockRequests[index], status };
    return mockRequests[index];
  },
};

// Real API реализация
const realApi = {
  async getAdminRequests(): Promise<CustomerRequest[]> {
    return apiClient.get<CustomerRequest[]>('/admin/customer-requests');
  },

  async updateRequestStatus(
    id: string,
    status: CustomerRequestStatus
  ): Promise<CustomerRequest> {
    return apiClient.patch<CustomerRequest>(
      `/admin/customer-requests/${id}/status`,
      { status }
    );
  },
};

// Экспортируем API в зависимости от конфигурации
export const customerRequestApi = config.USE_MOCK_API ? mockApi : realApi;