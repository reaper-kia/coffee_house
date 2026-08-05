import type { CartLine } from '../../app/providers/CartProvider';

export function calculateCartTotals(lines: CartLine[]): Record<string, number> {
  return lines.reduce<Record<string, number>>((totals, line) => {
    const currency = line.item.price_currency;
    totals[currency] = (totals[currency] ?? 0) + Number(line.item.price_amount) * line.quantity;
    return totals;
  }, {});
}
