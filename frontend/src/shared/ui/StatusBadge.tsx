import type { CustomerRequestStatus } from '../../entities/customer-request/model';

const labels = {
  ru: { NEW: 'Новая', CONFIRMED: 'Подтверждена', CANCELLED: 'Отменена', DONE: 'Завершена' },
  en: { NEW: 'New', CONFIRMED: 'Confirmed', CANCELLED: 'Cancelled', DONE: 'Completed' },
} as const;

export function StatusBadge({ status, language = 'ru' }: { status: CustomerRequestStatus; language?: 'ru' | 'en' }) {
  return <span className={`status-badge status-badge--${status.toLowerCase()}`}>{labels[language][status]}</span>;
}
