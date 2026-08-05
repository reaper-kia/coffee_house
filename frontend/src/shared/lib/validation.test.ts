import { describe, expect, it, vi } from 'vitest';
import { isFutureDateTime, isValidContact } from './validation';

describe('request validation', () => {
  it('accepts email or phone-like contacts', () => {
    expect(isValidContact('hello@ncnl.coffee')).toBe(true);
    expect(isValidContact('+44 20 7946 0842')).toBe(true);
    expect(isValidContact('abc')).toBe(false);
  });

  it('accepts only future local date times', () => {
    vi.setSystemTime(new Date('2029-01-01T12:00:00Z'));
    expect(isFutureDateTime('2030-01-01', '12:00')).toBe(true);
    expect(isFutureDateTime('2028-01-01', '12:00')).toBe(false);
    vi.useRealTimers();
  });
});
