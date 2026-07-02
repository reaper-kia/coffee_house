import { MenuCategory } from './types';

interface Props {
  categories: MenuCategory[];
  activeCategory: MenuCategory | 'all';
  onSelect: (category: MenuCategory | 'all') => void;
}

export const MenuCategoryFilter = ({ categories, activeCategory, onSelect }: Props) => (
  <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
    <button
      onClick={() => onSelect('all')}
      style={{
        padding: '8px 16px',
        borderRadius: '20px',
        border: 'none',
        background: activeCategory === 'all' ? '#007bff' : '#eee',
        color: activeCategory === 'all' ? 'white' : 'black',
        cursor: 'pointer',
      }}
    >
      Все
    </button>
    {categories.map((cat) => (
      <button
        key={cat}
        onClick={() => onSelect(cat)}
        style={{
          padding: '8px 16px',
          borderRadius: '20px',
          border: 'none',
          background: activeCategory === cat ? '#007bff' : '#eee',
          color: activeCategory === cat ? 'white' : 'black',
          cursor: 'pointer',
        }}
      >
        {cat === 'main' ? 'Основные' : cat === 'salad' ? 'Салаты' : cat === 'drink' ? 'Напитки' : 'Десерты'}
      </button>
    ))}
  </div>
);