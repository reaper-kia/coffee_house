import { createContext, useContext, useMemo, useState, type ReactNode } from 'react';

export type Language = 'ru' | 'en';

const dictionary = {
  ru: {
    home: 'Главная', menu: 'Меню', booking: 'Бронь', preorder: 'Предзаказ',
    events: 'Мероприятия', contacts: 'Контакты', cart: 'Корзина',
    bookTable: 'Забронировать столик', viewMenu: 'Смотреть меню', add: 'Добавить',
    loadMore: 'Загрузить ещё', search: 'Поиск по меню', allCategories: 'Всё меню',
    loading: 'Загрузка…', retry: 'Повторить', send: 'Отправить заявку',
    name: 'Ваше имя', contact: 'Телефон или email', date: 'Дата', time: 'Время',
    guests: 'Количество гостей', comment: 'Комментарий', optional: 'Необязательно',
    emptyCart: 'Корзина пока пуста', checkout: 'Оформить предзаказ', total: 'Итого',
    admin: 'Админка', logout: 'Выйти', refresh: 'Обновить', details: 'Подробнее',
    status: 'Статус', type: 'Тип заявки', all: 'Все', requests: 'Заявки клиентов',
    noRequests: 'Заявок по выбранным фильтрам нет', previous: 'Назад', next: 'Далее',
  },
  en: {
    home: 'Home', menu: 'Menu', booking: 'Booking', preorder: 'Pre-order',
    events: 'Events', contacts: 'Contact', cart: 'Basket',
    bookTable: 'Book a table', viewMenu: 'Explore menu', add: 'Add',
    loadMore: 'Load more', search: 'Search the menu', allCategories: 'All menu',
    loading: 'Loading…', retry: 'Try again', send: 'Send request',
    name: 'Your name', contact: 'Phone or email', date: 'Date', time: 'Time',
    guests: 'Number of guests', comment: 'Comment', optional: 'Optional',
    emptyCart: 'Your basket is empty', checkout: 'Place pre-order', total: 'Total',
    admin: 'Admin', logout: 'Log out', refresh: 'Refresh', details: 'Details',
    status: 'Status', type: 'Request type', all: 'All', requests: 'Customer requests',
    noRequests: 'No requests match these filters', previous: 'Previous', next: 'Next',
  },
} as const;

type TranslationKey = keyof typeof dictionary.ru;
interface LanguageContextValue {
  language: Language;
  setLanguage: (value: Language) => void;
  t: (key: TranslationKey) => string;
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>(() =>
    localStorage.getItem('ncnl-language') === 'en' ? 'en' : 'ru',
  );

  const value = useMemo<LanguageContextValue>(() => ({
    language,
    setLanguage: (next) => {
      localStorage.setItem('ncnl-language', next);
      setLanguageState(next);
    },
    t: (key) => dictionary[language][key],
  }), [language]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) throw new Error('useLanguage must be used inside LanguageProvider');
  return context;
}
