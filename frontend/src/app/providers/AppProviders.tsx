import type { ReactNode } from 'react';
import { CartProvider } from './CartProvider';
import { LanguageProvider } from './LanguageProvider';
import { ThemeProvider } from './ThemeProvider';
import { ToastProvider } from './ToastProvider';

export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <CartProvider>
          <ToastProvider>{children}</ToastProvider>
        </CartProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}
