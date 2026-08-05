import { useState, type FormEvent } from 'react';
import { CalendarHeart, GlassWater, UsersRound } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { customerRequestApi } from '../../entities/customer-request/api';
import { combineLocalDateTime, toLocalDateInput } from '../../shared/lib/format';
import { isFutureDateTime, isValidContact } from '../../shared/lib/validation';
import { Button } from '../../shared/ui/Button';
import { Input } from '../../shared/ui/Input';
import { Textarea } from '../../shared/ui/Textarea';

export function EventsPage() {
  const navigate = useNavigate();
  const { language, t } = useLanguage();
  const ru = language === 'ru';
  const [form, setForm] = useState({ name: '', contact: '', date: '', time: '', guests: '20', comment: '' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const guests = Number(form.guests);
    if (!form.name.trim() || !isValidContact(form.contact) || !isFutureDateTime(form.date, form.time) || guests < 1 || guests > 500) {
      setError(ru ? 'Проверьте имя, контакт, дату и количество гостей.' : 'Check the name, contact, date and guest count.'); return;
    }
    setSubmitting(true); setError('');
    try {
      const request = await customerRequestApi.create({
        request_type: 'EVENT_REQUEST', customer_name: form.name.trim(), contact: form.contact.trim(),
        desired_datetime: combineLocalDateTime(form.date, form.time), person_count: guests,
        comment: form.comment.trim() || null, items: [],
      });
      navigate('/success', { state: { request } });
    } catch (err) { setError(err instanceof Error ? err.message : 'Request failed'); }
    finally { setSubmitting(false); }
  };

  return (
    <section className="page-section event-page"><div className="container"><header className="event-hero"><div><p className="eyebrow">NCNL · Gatherings</p><h1>{ru ? 'Маленькие события с большим вниманием.' : 'Small gatherings, considered in every detail.'}</h1><p>{ru ? 'Ужины, дни рождения, презентации и встречи команд в отдельной части кофейни.' : 'Dinners, birthdays, launches and team gatherings in a private area of the coffee house.'}</p></div></header><div className="event-highlights"><div><CalendarHeart /><h3>{ru ? 'Гибкий формат' : 'Flexible format'}</h3><p>{ru ? 'От камерного завтрака до вечернего приёма.' : 'From an intimate breakfast to an evening reception.'}</p></div><div><GlassWater /><h3>{ru ? 'Меню под вас' : 'A menu for you'}</h3><p>{ru ? 'Кофе-бар, выпечка, канапе или общий ужин.' : 'Coffee bar, bakery, canapés or a shared dinner.'}</p></div><div><UsersRound /><h3>{ru ? 'До 60 гостей' : 'Up to 60 guests'}</h3><p>{ru ? 'Для больших форматов обсудим отдельное решение.' : 'We can discuss a tailored option for larger plans.'}</p></div></div><div className="form-page__grid event-form-section"><div className="form-page__intro"><p className="eyebrow eyebrow--dark">{ru ? 'Расскажите о событии' : 'Tell us about your event'}</p><h2>{ru ? 'Начнём с нескольких деталей' : 'A few details to get started'}</h2><p>{ru ? 'Администратор свяжется с вами и предложит формат, меню и предварительную стоимость.' : 'Our manager will contact you with a format, menu and initial estimate.'}</p></div><form className="request-form" onSubmit={submit}><div className="form-grid"><Input label={t('name')} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /><Input label={t('contact')} value={form.contact} onChange={(e) => setForm({ ...form, contact: e.target.value })} required /><Input label={t('date')} type="date" min={toLocalDateInput()} value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} required /><Input label={t('time')} type="time" value={form.time} onChange={(e) => setForm({ ...form, time: e.target.value })} required /><Input label={t('guests')} type="number" min="1" max="500" value={form.guests} onChange={(e) => setForm({ ...form, guests: e.target.value })} required /><Textarea label={ru ? 'Формат и пожелания' : 'Format and wishes'} value={form.comment} maxLength={2000} onChange={(e) => setForm({ ...form, comment: e.target.value })} required /></div>{error && <p className="form-error">{error}</p>}<Button type="submit" loading={submitting}>{t('send')}</Button></form></div></div></section>
  );
}
