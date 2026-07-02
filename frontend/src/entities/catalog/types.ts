export type MenuCategory = 'main' | 'salad' | 'drink' | 'dessert';

export interface MenuItem {
  id: string;
  name: string;
  price: number;
  category: MenuCategory;
  description?: string;
  image?: string;
}