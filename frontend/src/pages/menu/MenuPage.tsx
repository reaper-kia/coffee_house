import { useState, useEffect } from 'react';
import { catalogApi } from '../../entities/catalog/api';
import { MenuItem, MenuCategory } from '../../entities/catalog/types';
import { MenuItemCard } from '../../entities/catalog/MenuItemCard';
import { MenuCategoryFilter } from '../../entities/catalog/MenuCategoryFilter';
import { Loading } from '../../shared/ui/Loading';
import { ErrorMessage } from '../../shared/ui/ErrorMessage';

export const MenuPage = () => {
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState<MenuCategory | 'all'>('all');

  useEffect(() => {
    catalogApi
      .getMenu()
      .then((data) => setMenu(data))
      .catch(() => setError('Не удалось загрузить меню'))
      .finally(() => setLoading(false));
  }, []);

  const categories = Array.from(new Set(menu.map((item) => item.category)));
  const filteredMenu = activeCategory === 'all' ? menu : menu.filter((item) => item.category === activeCategory);

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Наше меню</h1>
      <MenuCategoryFilter categories={categories} activeCategory={activeCategory} onSelect={setActiveCategory} />
      {filteredMenu.map((item) => (
        <MenuItemCard key={item.id} item={item} />
      ))}
    </div>
  );
};