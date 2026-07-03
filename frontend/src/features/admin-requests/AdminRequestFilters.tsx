import type { FilterValue } from './adminRequestFilters';

interface Props {
  currentFilter: FilterValue;
  onFilterChange: (filter: FilterValue) => void;
}

const filterOptions: { value: FilterValue; label: string }[] = [
  { value: 'all', label: 'Все' },
  { value: 'new', label: 'Новые' },
  { value: 'in_progress', label: 'В работе' },
  { value: 'approved', label: 'Подтверждённые' },
  { value: 'rejected', label: 'Отклонённые' },
];

export const AdminRequestFilters = ({ currentFilter, onFilterChange }: Props) => (
  <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
    {filterOptions.map((opt) => (
      <button
        key={opt.value}
        onClick={() => onFilterChange(opt.value)}
        style={{
          padding: '8px 16px',
          borderRadius: '20px',
          border: 'none',
          background: currentFilter === opt.value ? '#007bff' : '#eee',
          color: currentFilter === opt.value ? 'white' : 'black',
          cursor: 'pointer',
          fontSize: '14px',
        }}
      >
        {opt.label}
      </button>
    ))}
  </div>
);