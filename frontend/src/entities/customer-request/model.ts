export type CustomerRequestType = 'TABLE_BOOKING' | 'PREORDER' | 'EVENT_REQUEST';
export type CustomerRequestStatus = 'NEW' | 'CONFIRMED' | 'CANCELLED' | 'DONE';

export interface CustomerRequestItem {
  menu_item_id: string;
  title: string;
  quantity: number;
  price_amount: string | number;
  price_currency: string;
  comment: string | null;
}

export interface CustomerRequest {
  id: string;
  request_type: CustomerRequestType;
  customer_name: string;
  contact: string;
  telegram_chat_id: string | null;
  desired_datetime: string;
  person_count: number | null;
  comment: string | null;
  status: CustomerRequestStatus;
  items: CustomerRequestItem[];
  created_at: string;
  updated_at: string;
}

export interface CustomerRequestPage {
  items: CustomerRequest[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export const statusTransitions: Record<CustomerRequestStatus, CustomerRequestStatus[]> = {
  NEW: ['CONFIRMED', 'CANCELLED'],
  CONFIRMED: ['DONE', 'CANCELLED'],
  CANCELLED: [],
  DONE: [],
};
