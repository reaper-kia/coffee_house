import type { CustomerRequest, CustomerRequestStatus } from '../../entities/customer-request/model';
import { StatusBadge } from '../../shared/ui/StatusBadge';
import { AdminRequestStatusSelect } from './AdminRequestStatusSelect';

interface Props {
  request: CustomerRequest;
  onStatusChange: (requestId: string, newStatus: CustomerRequestStatus) => void;
}

const typeLabels: Record<CustomerRequest['type'], string> = {
  booking: 'Бронь столика',
  preorder: 'Предзаказ',
  question: 'Вопрос',
};

export const AdminRequestCard = ({ request, onStatusChange }: Props) => {
  const formattedDate = new Date(request.createdAt).toLocaleString('ru-RU');

  return (
    <div
      style={{
        border: '1px solid #ddd',
        borderRadius: '10px',
        padding: '20px',
        marginBottom: '15px',
        background: '#fff',
        boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
        <h3 style={{ margin: 0 }}>{request.customerName}</h3>
        <StatusBadge status={request.status} />
      </div>

      <div style={{ color: '#666', marginBottom: '8px' }}>
        <strong>Тип:</strong> {typeLabels[request.type]}
      </div>
      <div style={{ color: '#666', marginBottom: '8px' }}>
        <strong>Контакт:</strong> {request.contact}
      </div>
      {request.desiredDatetime && (
        <div style={{ color: '#666', marginBottom: '8px' }}>
          <strong>Дата/время:</strong> {new Date(request.desiredDatetime).toLocaleString('ru-RU')}
        </div>
      )}
      {request.personCount && (
        <div style={{ color: '#666', marginBottom: '8px' }}>
          <strong>Гостей:</strong> {request.personCount}
        </div>
      )}
      {request.itemsCount && (
        <div style={{ color: '#666', marginBottom: '8px' }}>
          <strong>Товаров:</strong> {request.itemsCount}
        </div>
      )}
      {request.comment && (
        <div style={{ color: '#666', marginBottom: '8px' }}>
          <strong>Комментарий:</strong> {request.comment}
        </div>
      )}
      <div style={{ color: '#999', fontSize: '12px', marginBottom: '15px' }}>
        Создана: {formattedDate}
      </div>

      <AdminRequestStatusSelect
        requestId={request.id}
        currentStatus={request.status}
        onStatusChange={onStatusChange}
      />
    </div>
  );
};