import { describe, expect, it } from 'vitest';
import { statusTransitions } from './model';

describe('customer request status transitions', () => {
  it('mirrors the backend domain rules', () => {
    expect(statusTransitions.NEW).toEqual(['CONFIRMED', 'CANCELLED']);
    expect(statusTransitions.CONFIRMED).toEqual(['DONE', 'CANCELLED']);
    expect(statusTransitions.CANCELLED).toEqual([]);
    expect(statusTransitions.DONE).toEqual([]);
  });
});
