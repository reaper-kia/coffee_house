import { createContext, useContext, useMemo, useState, type ReactNode } from 'react';
import type { MenuItem } from '../../entities/catalog/types';

export interface CartLine { item: MenuItem; quantity: number }
interface CartContextValue {
  lines: CartLine[];
  itemCount: number;
  add: (item: MenuItem) => void;
  setQuantity: (id: string, quantity: number) => void;
  remove: (id: string) => void;
  clear: () => void;
}

const CartContext = createContext<CartContextValue | null>(null);
const STORAGE_KEY = 'ncnl-cart-v1';

function readCart(): CartLine[] {
  try {
    const value = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]');
    return Array.isArray(value) ? value : [];
  } catch {
    return [];
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [lines, setLines] = useState<CartLine[]>(readCart);

  const commit = (next: CartLine[]) => {
    setLines(next);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  };

  const value = useMemo<CartContextValue>(() => ({
    lines,
    itemCount: lines.reduce((sum, line) => sum + line.quantity, 0),
    add: (item) => commit(lines.some((line) => line.item.id === item.id)
      ? lines.map((line) => line.item.id === item.id
        ? { ...line, quantity: Math.min(100, line.quantity + 1) }
        : line)
      : [...lines, { item, quantity: 1 }]),
    setQuantity: (id, quantity) => commit(lines.map((line) =>
      line.item.id === id ? { ...line, quantity: Math.max(1, Math.min(100, quantity)) } : line,
    )),
    remove: (id) => commit(lines.filter((line) => line.item.id !== id)),
    clear: () => commit([]),
  }), [lines]);

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used inside CartProvider');
  return context;
}
