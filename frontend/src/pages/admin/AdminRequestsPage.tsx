import { useState, useEffect } from 'react';
import { customerRequestApi } from '../../entities/customer-request/api';
import type { CustomerRequest, CustomerRequestStatus } from '../../entities/customer-request/model';
import { AdminRequestsList } from '../../features/admin-requests/AdminRequestsList';
import { AdminRequestFilters } from '../../features/admin-requests/AdminRequestFilters';
import { filterAdminRequestsByStatus, type FilterValue } from '../../features/admin-requests/requestFilters';
import { Loading } from '../../shared/ui/Loading';
import { ErrorMessage } from '../../shared/ui/ErrorMessage';

export const AdminRequestsPage = () => {
  const [requests, setRequests] = useState<CustomerRequest[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentFilter, setCurrentFilter] = useState<FilterValue>('all');

  // Загрузка заявок
  useEffect(() => {
    const fetchRequests = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await customerRequestApi.getAdminRequests();
        setRequests(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Не удалось загрузить заявки');
      } finally {
        setIsLoading(false);
      }
    };

    fetchRequests();
  }, []);

  // Обработчик смены статуса
  const handleStatusChange = async (requestId: string, newStatus: CustomerRequestStatus) => {
  try {
    const updated = await customerRequestApi.updateRequestStatus(requestId, newStatus);
    setRequests((prev) =>
      prev.map((req) => (req.id === updated.id ? updated : req))
    );
  } catch (err) {
    // Ошибка уже обработана в AdminRequestStatusSelect
    throw err;
  }
};

  // Применяем фильтр
  const filteredRequests = filterAdminRequestsByStatus(requests, currentFilter);

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <h1>📋 Заявки клиентов</h1>

      {isLoading && <Loading />}
      {error && (
  <div>
    <ErrorMessage message={error} />
    <button
      onClick={() => window.location.reload()}
      style={{
        padding: '8px 16px',
        background: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        marginTop: '10px',
      }}
    >
      Попробовать снова
    </button>
  </div>
)}

      {!isLoading && !error && (
        <>
          <AdminRequestFilters
            currentFilter={currentFilter}
            onFilterChange={setCurrentFilter}
          />
          <AdminRequestsList
            requests={filteredRequests}
            onStatusChange={handleStatusChange}
          />
        </>
      )}
    </div>
  );
};