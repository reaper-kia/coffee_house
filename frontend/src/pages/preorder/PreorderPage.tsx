import { useMemo, useState, type FormEvent } from 'react';
import { Minus, Plus, ShoppingBag, Trash2 } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../app/providers/CartProvider';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { customerRequestApi } from '../../entities/customer-request/api';
import { calculateCartTotals } from '../../features/preorder/cartTotals';
import { combineLocalDateTime, formatMoney, toLocalDateInput } from '../../shared/lib/format';
import { isFutureDateTime, isValidContact } from '../../shared/lib/validation';
import { Button } from '../../shared/ui/Button';
import { EmptyState } from '../../shared/ui/EmptyState';
import { Input } from '../../shared/ui/Input';
import { Textarea } from '../../shared/ui/Textarea';

export function PreorderPage() {
  const navigate = useNavigate();
  const { lines, setQuantity, remove, clear } = useCart();
  const { language, t } = useLanguage();
  const ru = language === 'ru';
  const [form, setForm] = useState({ name: '', contact: '', date: '', time: '', comment: '' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const totals = useMemo(() => calculateCartTotals(lines), [lines]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!lines.length) { setError(ru ? 'Добавьте блюда в корзину.' : 'Add items to your basket.'); return; }
    if (!form.name.trim() || !isValidContact(form.contact) || !isFutureDateTime(form.date, form.time)) {
      setError(ru ? 'Проверьте имя, контакт, дату и время получения.' : 'Check your name, contact, collection date and time.'); return;
    }
    setSubmitting(true); setError('');
    try {
      const request = await customerRequestApi.create({
        request_type: 'PREORDER', customer_name: form.name.trim(), contact: form.contact.trim(),
        desired_datetime: combineLocalDateTime(form.date, form.time), person_count: null,
        comment: form.comment.trim() || null,
        items: lines.map((line) => ({ menu_item_id: line.item.id, quantity: line.quantity })),
      });
      clear();
      navigate('/success', { state: { request } });
    } catch (err) { setError(err instanceof Error ? err.message : 'Request failed'); }
    finally { setSubmitting(false); }
  };

  return (
    <section className="page-section cart-page"><div className="container"><header className="page-heading"><p className="eyebrow eyebrow--dark">NCNL · Collect</p><h1>{ru ? 'Предзаказ' : 'Pre-order'}</h1><p>{ru ? 'Соберите заказ заранее — мы приготовим его к выбранному времени.' : 'Build your order ahead and we will have it ready at your chosen time.'}</p></header>{lines.length === 0 ? <EmptyState title={t('emptyCart')} message={ru ? 'Выберите кофе, выпечку или завтрак в меню.' : 'Choose coffee, pastries or breakfast from the menu.'} action={<Link className="button button--primary" to="/menu">{t('viewMenu')}</Link>} /> : <form className="checkout-grid" onSubmit={submit}><div className="cart-lines">{lines.map((line) => <article className="cart-line" key={line.item.id}><img src={line.item.image_url || '/images/ncnl-pastry.webp'} onError={(event) => { event.currentTarget.src = '/images/ncnl-pastry.webp'; }} alt="" /><div className="cart-line__main"><h2>{line.item.title}</h2><span>{formatMoney(line.item.price_amount, line.item.price_currency, ru ? 'ru-RU' : 'en-GB')}</span></div><div className="quantity"><button type="button" onClick={() => setQuantity(line.item.id, line.quantity - 1)} aria-label="Decrease"><Minus size={15} /></button><span>{line.quantity}</span><button type="button" onClick={() => setQuantity(line.item.id, line.quantity + 1)} aria-label="Increase"><Plus size={15} /></button></div><button className="cart-line__remove" type="button" onClick={() => remove(line.item.id)} aria-label="Remove"><Trash2 size={18} /></button></article>)}</div><aside className="checkout-panel"><div className="checkout-panel__title"><ShoppingBag /><h2>{ru ? 'Оформление' : 'Collection details'}</h2></div><div className="form-grid"><Input label={t('name')} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /><Input label={t('contact')} value={form.contact} onChange={(e) => setForm({ ...form, contact: e.target.value })} required /><Input label={t('date')} type="date" min={toLocalDateInput()} value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} required /><Input label={t('time')} type="time" value={form.time} onChange={(e) => setForm({ ...form, time: e.target.value })} required /><Textarea label={`${t('comment')} · ${t('optional')}`} value={form.comment} maxLength={2000} onChange={(e) => setForm({ ...form, comment: e.target.value })} /></div><div className="checkout-total"><span>{t('total')}</span><div>{Object.entries(totals).map(([currency, amount]) => <strong key={currency}>{formatMoney(amount, currency, ru ? 'ru-RU' : 'en-GB')}</strong>)}</div></div>{error && <p className="form-error">{error}</p>}<Button type="submit" loading={submitting}>{t('checkout')}</Button></aside></form>}</div></section>
  );
}
