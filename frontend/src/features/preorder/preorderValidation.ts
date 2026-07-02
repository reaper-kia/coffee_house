export interface PreorderFormValues {
  name: string;
  phone: string;
  pickupDate: string;
  pickupTime: string;
  items: { menuItemId: string; quantity: number }[];
  comment?: string;
}

export interface PreorderErrors {
  name?: string;
  phone?: string;
  pickupDate?: string;
  pickupTime?: string;
  items?: string;
}

export const validatePreorder = (values: PreorderFormValues): PreorderErrors => {
  const errors: PreorderErrors = {};

  if (!values.name.trim()) errors.name = 'Введите ваше имя';
  const phoneDigits = values.phone.replace(/\D/g, '');
  if (phoneDigits.length < 10) errors.phone = 'Введите корректный номер телефона';
  if (!values.pickupDate) errors.pickupDate = 'Выберите дату получения';
  if (!values.pickupTime) errors.pickupTime = 'Выберите время получения';
  if (values.items.length === 0) errors.items = 'Выберите хотя бы одно блюдо';

  return errors;
};