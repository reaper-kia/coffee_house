import { describe, expect, it } from 'vitest';
import type { CartLine } from '../../app/providers/CartProvider';
import { calculateCartTotals } from './cartTotals';

const baseItem = {
  id: '1', category_id: null, category_title: null, title: 'Flat white', description: null,
  price_amount: '4.50', price_currency: 'EUR', image_url: null, is_available: true, position: 1,
};

describe('calculateCartTotals', () => {
  it('keeps totals separate by backend currency', () => {
    const lines: CartLine[] = [
      { item: baseItem, quantity: 2 },
      { item: { ...baseItem, id: '2', price_amount: '3', price_currency: 'USD' }, quantity: 1 },
    ];
    expect(calculateCartTotals(lines)).toEqual({ EUR: 9, USD: 3 });
  });
});
