import { useState, type FormEvent } from 'react';
import { CalendarDays, Clock3, Users } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { customerRequestApi } from '../../entities/customer-request/api';
import { combineLocalDateTime, toLocalDateInput } from '../../shared/lib/format';
import { isFutureDateTime, isValidContact } from '../../shared/lib/validation';
import { Button } from '../../shared/ui/Button';
import { Input } from '../../shared/ui/Input';
import { Textarea } from '../../shared/ui/Textarea';

export function BookingPage() {
  const navigate = useNavigate();
  const { language, t } = useLanguage();
  const ru = language === 'ru';
  const [form, setForm] = useState({ name: '', contact: '', date: '', time: '', guests: '2', comment: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const next: Record<string, string> = {};
    if (!form.name.trim()) next.name = ru ? 'Введите имя' : 'Enter your name';
    if (!isValidContact(form.contact)) next.contact = ru ? 'Укажите телефон или email' : 'Enter a phone number or email';
    if (!isFutureDateTime(form.date, form.time)) next.date = ru ? 'Выберите будущие дату и время' : 'Choose a future date and time';
    const guests = Number(form.guests);
    if (!Number.isInteger(guests) || guests < 1 || guests > 20) next.guests = ru ? 'От 1 до 20 гостей' : 'Between 1 and 20 guests';
    setErrors(next);
    if (Object.keys(next).length) return;
    setSubmitting(true);
    try {
      const request = await customerRequestApi.create({
        request_type: 'TABLE_BOOKING', customer_name: form.name.trim(), contact: form.contact.trim(),
        desired_datetime: combineLocalDateTime(form.date, form.time), person_count: guests,
        comment: form.comment.trim() || null, items: [],
      });
      navigate('/success', { state: { request } });
    } catch (error) {
      setErrors({ form: error instanceof Error ? error.message : 'Request failed' });
    } finally { setSubmitting(false); }
  };

  return (
    <section className="page-section form-page">
      <div className="container form-page__grid">
        <div className="form-page__intro"><p className="eyebrow eyebrow--dark">NCNL · Table</p><h1>{ru ? 'Забронировать столик' : 'Book a table'}</h1><p>{ru ? 'Выберите удобное время. Мы подтвердим бронь по указанному контакту.' : 'Choose a time that suits you. We will confirm using the contact you provide.'}</p><div className="info-list"><div><CalendarDays /><span><strong>{ru ? 'Бронь онлайн' : 'Book online'}</strong>{ru ? 'до 20 гостей' : 'up to 20 guests'}</span></div><div><Clock3 /><span><strong>{ru ? 'Стол держим 15 минут' : '15-minute grace period'}</strong>{ru ? 'со времени бронирования' : 'from your booking time'}</span></div><div><Users /><span><strong>{ru ? 'Большие группы' : 'Larger groups'}</strong>{ru ? 'оформите заявку на мероприятие' : 'use our events request'}</span></div></div></div>
        <form className="request-form" onSubmit={submit} noValidate><div className="form-grid"><Input label={t('name')} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} error={errors.name} autoComplete="name" required /><Input label={t('contact')} value={form.contact} onChange={(e) => setForm({ ...form, contact: e.target.value })} error={errors.contact} placeholder="+44… / name@email.com" required /><Input label={t('date')} type="date" min={toLocalDateInput()} value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} error={errors.date} required /><Input label={t('time')} type="time" value={form.time} onChange={(e) => setForm({ ...form, time: e.target.value })} required /><Input label={t('guests')} type="number" min="1" max="20" value={form.guests} onChange={(e) => setForm({ ...form, guests: e.target.value })} error={errors.guests} required /><Textarea label={`${t('comment')} · ${t('optional')}`} value={form.comment} maxLength={2000} onChange={(e) => setForm({ ...form, comment: e.target.value })} /></div>{errors.form && <p className="form-error" role="alert">{errors.form}</p>}<Button type="submit" loading={submitting}>{t('send')}</Button><p className="form-note">{ru ? 'Отправляя заявку, вы соглашаетесь на обработку контактных данных для связи по бронированию.' : 'By submitting, you agree that we may use your contact details to manage this booking.'}</p></form>
      </div>
    </section>
  );
}
