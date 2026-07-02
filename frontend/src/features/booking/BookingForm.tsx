import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../../shared/ui/Input';
import { Button } from '../../shared/ui/Button';
import { customerRequestApi } from '../../entities/customer-request/api';
import { validateBooking, BookingFormValues, BookingErrors } from './bookingValidation';

export const BookingForm = () => {
  const navigate = useNavigate();
  const [values, setValues] = useState<BookingFormValues>({
    name: '', phone: '', date: '', time: '', guests: 1,
  });
  const [errors, setErrors] = useState<BookingErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setValues((prev) => ({
      ...prev,
      [name]: name === 'guests' ? Number(value) : value,
    }));
    // Убираем ошибку при изменении поля
    if (errors[name as keyof BookingErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const validationErrors = validateBooking(values);
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length === 0) {
      setIsSubmitting(true);
      try {
        await customerRequestApi.createBooking(values);
        navigate('/success');
      } catch (err) {
        alert('Ошибка при бронировании. Попробуйте позже.');
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '500px', margin: '0 auto' }}>
      <h2>Забронировать столик</h2>
      <Input label="Ваше имя" name="name" value={values.name} onChange={handleChange} error={errors.name} />
      <Input label="Телефон" name="phone" value={values.phone} onChange={handleChange} error={errors.phone} placeholder="+7..." />
      <Input label="Дата" name="date" type="date" value={values.date} onChange={handleChange} error={errors.date} />
      <Input label="Время" name="time" type="time" value={values.time} onChange={handleChange} error={errors.time} />
      <Input label="Количество гостей" name="guests" type="number" min="1" max="20" value={values.guests} onChange={handleChange} error={errors.guests} />
      
      <Button type="submit" disabled={isSubmitting} style={{ width: '100%' }}>
        {isSubmitting ? 'Бронируем...' : 'Забронировать'}
      </Button>
    </form>
  );
};