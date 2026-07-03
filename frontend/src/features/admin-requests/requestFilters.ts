import type { CustomerRequest, CustomerRequestStatus } from '../../entities/customer-request/model';

export type FilterValue = 'all' | CustomerRequestStatus;

export const filterAdminRequestsByStatus = (
  requests: CustomerRequest[],
  status: FilterValue
): CustomerRequest[] => {
  if (status === 'all') {
    return [...requests];
  }
  return requests.filter((req) => req.status === status);
};