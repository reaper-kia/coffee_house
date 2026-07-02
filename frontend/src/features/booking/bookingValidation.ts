export interface BookingFormValues {
  name: string;
  phone: string;
  date: string;
  time: string;
  guests: number;
}

export interface BookingErrors {
  name?: string;
  phone?: string;
  date?: string;
  time?: string;
  guests?: string;
}

export const validateBooking = (values: BookingFormValues): BookingErrors => {
  const errors: BookingErrors = {};

  if (!values.name.trim()) errors.name = 'Введите ваше имя';
  
  // Простая проверка телефона (минимум 10 цифр)
  const phoneDigits = values.phone.replace(/\D/g, '');
  if (phoneDigits.length < 10) errors.phone = 'Введите корректный номер телефона';

  if (!values.date) errors.date = 'Выберите дату';
  if (!values.time) errors.time = 'Выберите время';
  
  if (values.guests < 1) errors.guests = 'Минимум 1 гость';
  if (values.guests > 20) errors.guests = 'Максимум 20 гостей';

  return errors;
};