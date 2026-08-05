import { apiClient } from '../../shared/api/client';
import type {
  CustomerRequest,
  CustomerRequestPage,
  CustomerRequestStatus,
  CustomerRequestType,
} from './model';

export interface CreateCustomerRequestPayload {
  request_type: CustomerRequestType;
  customer_name: string;
  contact: string;
  telegram_chat_id?: string | null;
  desired_datetime: string;
  person_count?: number | null;
  comment?: string | null;
  items: Array<{ menu_item_id: string; quantity: number; comment?: string | null }>;
}

export interface AdminRequestQuery {
  status?: CustomerRequestStatus | 'ALL';
  requestType?: CustomerRequestType | 'ALL';
  page?: number;
  pageSize?: number;
  signal?: AbortSignal;
}

export const customerRequestApi = {
  create(payload: CreateCustomerRequestPayload): Promise<CustomerRequest> {
    return apiClient.post<CustomerRequest>('/api/v1/customer-requests', payload);
  },
  getAdminRequests(query: AdminRequestQuery = {}): Promise<CustomerRequestPage> {
    const params = new URLSearchParams({
      page: String(query.page ?? 1),
      page_size: String(query.pageSize ?? 12),
    });
    if (query.status && query.status !== 'ALL') params.set('status', query.status);
    if (query.requestType && query.requestType !== 'ALL') params.set('request_type', query.requestType);
    return apiClient.get<CustomerRequestPage>(`/admin/customer-requests?${params}`, query.signal);
  },
  getById(id: string): Promise<CustomerRequest> {
    return apiClient.get<CustomerRequest>(`/admin/customer-requests/${id}`);
  },
  updateRequestStatus(id: string, status: CustomerRequestStatus): Promise<CustomerRequest> {
    const params = new URLSearchParams({ status });
    return apiClient.patch<CustomerRequest>(`/admin/customer-requests/${id}/status?${params}`);
  },
};
