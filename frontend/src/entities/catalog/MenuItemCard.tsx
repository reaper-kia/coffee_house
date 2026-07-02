import { MenuItem } from './types';

export const MenuItemCard = ({ item }: { item: MenuItem }) => (
  <div style={{ border: '1px solid #eee', borderRadius: '12px', padding: '15px', marginBottom: '15px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
    <h3 style={{ margin: '0 0 10px 0' }}>{item.name}</h3>
    <p style={{ color: '#666', margin: '0 0 10px 0' }}>{item.description}</p>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ fontWeight: 'bold', fontSize: '18px' }}>{item.price} руб.</span>
      <span style={{ background: '#f0f0f0', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>
        {item.category === 'main' ? 'Основное' : item.category === 'salad' ? 'Салат' : item.category === 'drink' ? 'Напиток' : 'Десерт'}
      </span>
    </div>
  </div>
);