// Типы заявок
export type CustomerRequestType = 'booking' | 'preorder' | 'question';

// Статусы заявок
export type CustomerRequestStatus =
  | 'new'
  | 'in_progress'
  | 'approved'
  | 'rejected';

// Интерфейс заявки
export interface CustomerRequest {
  id: string;
  type: CustomerRequestType;
  customerName: string;
  contact: string;
  desiredDatetime?: string;
  personCount?: number;
  itemsCount?: number;
  comment?: string;
  status: CustomerRequestStatus;
  createdAt: string;
}

// DTO для обновления статуса
export interface UpdateRequestStatusDto {
  id: string;
  status: CustomerRequestStatus;
}