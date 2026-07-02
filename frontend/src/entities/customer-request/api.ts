import type { CustomerRequest, CreateBookingDto, CreatePreorderDto } from './types';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

// хранилище заявок в памяти(мок)
let mockRequests: CustomerRequest[] = [
  // тестовые заявки
  {
    id: '1',
    type: 'booking',
    status: 'pending',
    createdAt: new Date().toISOString(),
    name: 'Иван Тестовый',
    phone: '+79991234567',
    date: '2026-07-05',
    time: '19:00',
    guests: 4,
  },
];

export const customerRequestApi = {
  async createBooking(dto: CreateBookingDto): Promise<CustomerRequest> {
    await delay(1000);
    const newRequest: CustomerRequest = {
      id: String(Date.now()),
      type: 'booking',
      status: 'pending',
      createdAt: new Date().toISOString(),
      ...dto,
    };
    mockRequests = [...mockRequests, newRequest];
    return newRequest;
  },

  async createPreorder(dto: CreatePreorderDto): Promise<CustomerRequest> {
    await delay(1000);
    const newRequest: CustomerRequest = {
      id: String(Date.now()),
      type: 'preorder',
      status: 'pending',
      createdAt: new Date().toISOString(),
      ...dto,
    };
    mockRequests = [...mockRequests, newRequest];
    return newRequest;
  },

  async getRequests(): Promise<CustomerRequest[]> {
    await delay(500);
    return mockRequests;
  },

  async updateStatus(id: string, status: CustomerRequest['status']): Promise<CustomerRequest> {
    await delay(500);
    const idx = mockRequests.findIndex((r) => r.id === id);
    if (idx === -1) throw new Error('Заявка не найдена');
    mockRequests[idx] = { ...mockRequests[idx], status };
    return mockRequests[idx];
  },
};