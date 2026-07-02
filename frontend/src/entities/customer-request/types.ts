export type RequestType = 'booking' | 'preorder';
export type RequestStatus = 'pending' | 'confirmed' | 'cancelled' | 'completed';

export interface CreateBookingDto {
  name: string;
  phone: string;
  date: string;
  time: string;
  guests: number;
}

export interface CreatePreorderDto {
  name: string;
  phone: string;
  pickupDate: string;
  pickupTime: string;
  items: { menuItemId: string; quantity: number }[];
  comment?: string;
}

export interface CustomerRequest {
  id: string;
  type: RequestType;
  status: RequestStatus;
  createdAt: string;
  // Поля брони
  name?: string;
  phone?: string;
  date?: string;
  time?: string;
  guests?: number;
  // Поля предзаказа
  pickupDate?: string;
  pickupTime?: string;
  items?: { menuItemId: string; quantity: number; name?: string; price?: number }[];
  comment?: string;
}