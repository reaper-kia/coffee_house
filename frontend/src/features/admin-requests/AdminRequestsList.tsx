import type { CustomerRequest, CustomerRequestStatus } from '../../entities/customer-request/model';
import { AdminRequestCard } from './AdminRequestCard';
import { EmptyState } from '../../shared/ui/EmptyState';

interface Props {
  requests: CustomerRequest[];
  onStatusChange: (requestId: string, newStatus: CustomerRequestStatus) => void;
}

export const AdminRequestsList = ({ requests, onStatusChange }: Props) => {
  if (requests.length === 0) {
    return <EmptyState message="Заявок пока нет" />;
  }

  return (
    <div>
      {requests.map((req) => (
        <AdminRequestCard key={req.id} request={req} onStatusChange={onStatusChange} />
      ))}
    </div>
  );
};