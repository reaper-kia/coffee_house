import { useState } from 'react';
import type { CustomerRequestStatus } from '../../entities/customer-request/model';
import { Select } from '../../shared/ui/Select';

interface Props {
  requestId: string;
  currentStatus: CustomerRequestStatus;
  onStatusChange: (requestId: string, newStatus: CustomerRequestStatus) => Promise<void>;
}

export const AdminRequestStatusSelect = ({ requestId, currentStatus, onStatusChange }: Props) => {
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const options = [
    { value: 'new', label: 'Новая' },
    { value: 'in_progress', label: 'В работе' },
    { value: 'approved', label: 'Подтверждена' },
    { value: 'rejected', label: 'Отклонена' },
  ];

  const handleChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newStatus = e.target.value as CustomerRequestStatus;
    
    // Подтверждение для критичных статусов
    if (newStatus === 'rejected' && currentStatus !== 'rejected') {
      const confirmed = window.confirm('Вы уверены, что хотите отклонить заявку?');
      if (!confirmed) {
        return; // Отмена изменения
      }
    }

    setIsUpdating(true);
    setError(null);

    try {
      await onStatusChange(requestId, newStatus);
    } catch (err) {
      console.error('Ошибка обновления статуса:', err);
      setError('Не удалось обновить статус');
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div>
      <Select
        label="Изменить статус:"
        options={options}
        value={currentStatus}
        onChange={handleChange}
        disabled={isUpdating}
      />
      {isUpdating && (
        <span style={{ color: '#007bff', fontSize: '12px', marginLeft: '10px' }}>
          Обновление...
        </span>
      )}
      {error && (
        <span style={{ color: '#dc3545', fontSize: '12px', marginLeft: '10px' }}>
          {error}
        </span>
      )}
    </div>
  );
};