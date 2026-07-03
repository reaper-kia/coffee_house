import type { CustomerRequestStatus } from '../../entities/customer-request/model';

const statusConfig: Record<CustomerRequestStatus, { label: string; color: string; background: string }> = {
  new: { label: 'Новая', color: '#fff', background: '#007bff' },
  in_progress: { label: 'В работе', color: '#fff', background: '#ffc107' },
  approved: { label: 'Подтверждена', color: '#fff', background: '#28a745' },
  rejected: { label: 'Отклонена', color: '#fff', background: '#dc3545' },
};

export const StatusBadge = ({ status }: { status: CustomerRequestStatus }) => {
  const config = statusConfig[status];
  return (
    <span
      style={{
        display: 'inline-block',
        padding: '4px 10px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        color: config.color,
        background: config.background,
      }}
    >
      {config.label}
    </span>
  );
};