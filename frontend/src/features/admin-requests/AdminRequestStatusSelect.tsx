import type { CustomerRequestStatus } from '../../entities/customer-request/model';
import { Select } from '../../shared/ui/Select';

interface Props {
  requestId: string;
  currentStatus: CustomerRequestStatus;
  onStatusChange: (requestId: string, newStatus: CustomerRequestStatus) => void;
}

export const AdminRequestStatusSelect = ({ requestId, currentStatus, onStatusChange }: Props) => {
  const options = [
    { value: 'new', label: 'Новая' },
    { value: 'in_progress', label: 'В работе' },
    { value: 'approved', label: 'Подтверждена' },
    { value: 'rejected', label: 'Отклонена' },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onStatusChange(requestId, e.target.value as CustomerRequestStatus);
  };

  return (
    <Select
      label="Изменить статус:"
      options={options}
      value={currentStatus}
      onChange={handleChange}
    />
  );
};