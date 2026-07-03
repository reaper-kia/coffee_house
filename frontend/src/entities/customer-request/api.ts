import type { CustomerRequest, CustomerRequestStatus } from './model';
import { mockCustomerRequests } from './mockData';

// ============================================
// TEMPORARY MOCK API
// ============================================

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

// Рабочая копия mock-данных (чтобы можно было менять статусы)
let requests = [...mockCustomerRequests];

export const customerRequestApi = {
  // Получить все заявки для админки
  async getAdminRequests(): Promise<CustomerRequest[]> {
    await delay(600);
    // Имитация случайной ошибки для проверки error state (10% шанс)
    if (Math.random() < 0.02) {
      throw new Error('Не удалось загрузить заявки');
    }
    return requests;
  },

  // Обновить статус заявки
  async updateRequestStatus(
    id: string,
    status: CustomerRequestStatus
  ): Promise<CustomerRequest> {
    await delay(400);
    const index = requests.findIndex((r) => r.id === id);
    if (index === -1) {
      throw new Error('Заявка не найдена');
    }
    requests[index] = { ...requests[index], status };
    return requests[index];
  },

  async createBooking(dto: any): Promise<CustomerRequest> {
    await delay(1000);
    const newRequest: CustomerRequest = {
      id: String(Date.now()),
      type: 'booking',
      status: 'new',
      createdAt: new Date().toISOString(),
      customerName: dto.name,
      contact: dto.phone,
      desiredDatetime: `${dto.date}T${dto.time}:00`,
      personCount: dto.guests,
    };
    requests = [...requests, newRequest];
    return newRequest;
  },

  async createPreorder(dto: any): Promise<CustomerRequest> {
    await delay(1000);
    const newRequest: CustomerRequest = {
      id: String(Date.now()),
      type: 'preorder',
      status: 'new',
      createdAt: new Date().toISOString(),
      customerName: dto.name,
      contact: dto.phone,
      desiredDatetime: `${dto.pickupDate}T${dto.pickupTime}:00`,
      itemsCount: dto.items?.reduce((sum: number, i: any) => sum + i.quantity, 0) || 0,
      comment: dto.comment,
    };
    requests = [...requests, newRequest];
    return newRequest;
  },
};