import { MenuItem } from '../../entities/catalog/types';

interface Props {
  menu: MenuItem[];
  selectedItems: { menuItemId: string; quantity: number }[];
}

export const SelectedPreorderItems = ({ menu, selectedItems }: Props) => {
  if (selectedItems.length === 0) return <p>Ничего не выбрано</p>;

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {selectedItems.map((item) => {
        const menuItem = menu.find((m) => m.id === item.menuItemId);
        if (!menuItem) return null;
        return (
          <li key={item.menuItemId} style={{ marginBottom: '10px', padding: '10px', background: '#f8f9fa', borderRadius: '8px' }}>
            <b>{menuItem.name}</b> x {item.quantity} = {menuItem.price * item.quantity} руб.
          </li>
        );
      })}
    </ul>
  );
};