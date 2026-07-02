import type { MenuItem } from './types';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const mockMenu: MenuItem[] = [
  { id: '1', name: 'Пицца Маргарита', price: 500, category: 'main', description: 'Томаты, моцарелла, базилик' },
  { id: '2', name: 'Цезарь с курицей', price: 350, category: 'salad', description: 'Курица, салат, соус' },
  { id: '3', name: 'Тирамису', price: 280, category: 'dessert', description: 'Классический итальянский десерт' },
  { id: '4', name: 'Кола', price: 150, category: 'drink', description: '0.5 л' },
  { id: '5', name: 'Кофе латте', price: 220, category: 'drink', description: '300 мл' },
];

export const catalogApi = {
  async getMenu(): Promise<MenuItem[]> {
    await delay(800); // имитируем задержку сети
    return mockMenu;
  },

  async getById(id: string): Promise<MenuItem | undefined> {
    await delay(300);
    return mockMenu.find((item) => item.id === id);
  },
};