import { useCallback, useEffect, useMemo, useState } from 'react';
import { CalendarClock, CheckCircle2, ChevronLeft, ChevronRight, ClipboardList, LogOut, RefreshCw, Search, SlidersHorizontal, Users, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { useToast } from '../../app/providers/ToastProvider';
import { customerRequestApi } from '../../entities/customer-request/api';
import { statusTransitions, type CustomerRequest, type CustomerRequestStatus, type CustomerRequestType } from '../../entities/customer-request/model';
import { authApi } from '../../features/auth/api';
import { ApiError } from '../../shared/api/client';
import { config } from '../../shared/config/env';
import { formatDateTime, formatMoney } from '../../shared/lib/format';
import { Button } from '../../shared/ui/Button';
import { EmptyState } from '../../shared/ui/EmptyState';
import { ErrorMessage } from '../../shared/ui/ErrorMessage';
import { Loading } from '../../shared/ui/Loading';
import { Select } from '../../shared/ui/Select';
import { StatusBadge } from '../../shared/ui/StatusBadge';

const typeLabels = {
  ru: { TABLE_BOOKING: 'Бронь столика', PREORDER: 'Предзаказ', EVENT_REQUEST: 'Мероприятие' },
  en: { TABLE_BOOKING: 'Table booking', PREORDER: 'Pre-order', EVENT_REQUEST: 'Event' },
} as const;
const statusLabels = {
  ru: { ALL: 'Все статусы', NEW: 'Новые', CONFIRMED: 'Подтверждённые', CANCELLED: 'Отменённые', DONE: 'Завершённые' },
  en: { ALL: 'All statuses', NEW: 'New', CONFIRMED: 'Confirmed', CANCELLED: 'Cancelled', DONE: 'Completed' },
} as const;

export function AdminRequestsPage() {
  const navigate = useNavigate();
  const { language, t } = useLanguage();
  const { showToast } = useToast();
  const ru = language === 'ru';
  const [items, setItems] = useState<CustomerRequest[]>([]);
  const [status, setStatus] = useState<CustomerRequestStatus | 'ALL'>('ALL');
  const [requestType, setRequestType] = useState<CustomerRequestType | 'ALL'>('ALL');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState<CustomerRequest | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState('');
  const [updatingId, setUpdatingId] = useState('');
  const [updatedAt, setUpdatedAt] = useState<Date | null>(null);

  const load = useCallback(async (quiet = false) => {
    if (quiet) setRefreshing(true);
    else setLoading(true);
    setError('');
    try {
      const result = await customerRequestApi.getAdminRequests({ status, requestType, page, pageSize: 12 });
      setItems(result.items); setTotal(result.total); setTotalPages(result.total_pages); setUpdatedAt(new Date());
      setSelected((current) => current ? result.items.find((item) => item.id === current.id) ?? current : null);
    } catch (err) {
      if (err instanceof ApiError && (err.status === 401 || err.status === 403)) { navigate('/admin/login', { replace: true }); return; }
      setError(err instanceof Error ? err.message : 'Request failed');
    } finally { setLoading(false); setRefreshing(false); }
  }, [navigate, page, requestType, status]);

  useEffect(() => { void load(); }, [load]);
  useEffect(() => {
    const timer = window.setInterval(() => { if (!document.hidden) void load(true); }, config.adminPollingMs);
    return () => window.clearInterval(timer);
  }, [load]);

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return items;
    return items.filter((item) => `${item.customer_name} ${item.contact} ${item.id}`.toLowerCase().includes(query));
  }, [items, search]);

  const changeStatus = async (request: CustomerRequest, next: CustomerRequestStatus) => {
    if ((next === 'CANCELLED' || next === 'DONE') && !window.confirm(ru ? 'Подтвердить изменение статуса?' : 'Confirm this status change?')) return;
    setUpdatingId(request.id);
    try {
      const updated = await customerRequestApi.updateRequestStatus(request.id, next);
      setItems((current) => current.map((item) => item.id === updated.id ? updated : item));
      setSelected((current) => current?.id === updated.id ? updated : current);
      showToast(ru ? 'Статус заявки обновлён' : 'Request status updated');
    } catch (err) { showToast(err instanceof Error ? err.message : 'Update failed', 'error'); }
    finally { setUpdatingId(''); }
  };

  const logout = async () => { try { await authApi.logout(); } finally { navigate('/admin/login', { replace: true }); } };

  return (
    <div className="admin-shell">
      <aside className="admin-sidebar"><div className="brand brand--admin"><span className="brand__mark">NCNL</span><span className="brand__caption">Admin</span></div><nav><a className="active"><ClipboardList />{t('requests')}<span>{total}</span></a></nav><div className="admin-sidebar__footer"><button type="button" onClick={logout}><LogOut />{t('logout')}</button></div></aside>
      <main className="admin-main"><header className="admin-header"><div><p className="eyebrow eyebrow--dark">NCNL · Operations</p><h1>{t('requests')}</h1><p>{updatedAt ? `${ru ? 'Обновлено' : 'Updated'} ${updatedAt.toLocaleTimeString(ru ? 'ru-RU' : 'en-GB', { hour: '2-digit', minute: '2-digit' })}` : '—'} · {ru ? 'автообновление 25 сек.' : 'auto-refresh 25 sec.'}</p></div><Button variant="secondary" loading={refreshing} onClick={() => void load(true)}><RefreshCw size={17} /> {t('refresh')}</Button></header>
        <section className="admin-stats"><article><span><ClipboardList /></span><div><small>{ru ? 'Всего по фильтру' : 'Filtered total'}</small><strong>{total}</strong></div></article><article><span><CalendarClock /></span><div><small>{ru ? 'Новых на странице' : 'New on page'}</small><strong>{items.filter((item) => item.status === 'NEW').length}</strong></div></article><article><span><CheckCircle2 /></span><div><small>{ru ? 'Подтверждено' : 'Confirmed'}</small><strong>{items.filter((item) => item.status === 'CONFIRMED').length}</strong></div></article></section>
        <section className="admin-panel"><div className="admin-filters"><span className="admin-filters__label"><SlidersHorizontal /> {ru ? 'Фильтры' : 'Filters'}</span><Select aria-label={t('status')} value={status} onChange={(event) => { setStatus(event.target.value as CustomerRequestStatus | 'ALL'); setPage(1); }} options={(Object.keys(statusLabels[language]) as Array<keyof typeof statusLabels.ru>).map((value) => ({ value, label: statusLabels[language][value] }))} /><Select aria-label={t('type')} value={requestType} onChange={(event) => { setRequestType(event.target.value as CustomerRequestType | 'ALL'); setPage(1); }} options={[{ value: 'ALL', label: ru ? 'Все типы' : 'All types' }, ...Object.entries(typeLabels[language]).map(([value, label]) => ({ value, label }))]} /><label className="search-field admin-search"><Search size={17} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder={ru ? 'Имя, контакт или ID' : 'Name, contact or ID'} /></label></div>
          {loading && <Loading />}{!loading && error && <ErrorMessage message={error} onRetry={() => void load()} />}{!loading && !error && filtered.length === 0 && <EmptyState title={t('noRequests')} />}
          {!loading && !error && filtered.length > 0 && <div className="request-table"><div className="request-table__head"><span>{ru ? 'Клиент' : 'Customer'}</span><span>{t('type')}</span><span>{ru ? 'Дата визита' : 'Visit date'}</span><span>{t('status')}</span><span /></div>{filtered.map((request) => <button className="request-row" key={request.id} type="button" onClick={() => setSelected(request)}><span><b>{request.customer_name}</b><small>{request.contact}</small></span><span>{typeLabels[language][request.request_type]}</span><span>{formatDateTime(request.desired_datetime, ru ? 'ru-RU' : 'en-GB')}</span><span><StatusBadge status={request.status} language={language} /></span><span><ChevronRight /></span></button>)}</div>}
          {!loading && !error && totalPages > 1 && <div className="pagination"><Button variant="ghost" disabled={page <= 1} onClick={() => setPage((value) => value - 1)}><ChevronLeft />{t('previous')}</Button><span>{ru ? 'Страница' : 'Page'} {page} / {totalPages}</span><Button variant="ghost" disabled={page >= totalPages} onClick={() => setPage((value) => value + 1)}>{t('next')}<ChevronRight /></Button></div>}
        </section>
      </main>

      {selected && <div className="drawer-backdrop" onMouseDown={() => setSelected(null)}><aside className="request-drawer" role="dialog" aria-modal="true" aria-labelledby="request-title" onMouseDown={(event) => event.stopPropagation()}><header><div><p>#{selected.id.slice(0, 8).toUpperCase()}</p><h2 id="request-title">{selected.customer_name}</h2></div><button type="button" onClick={() => setSelected(null)} aria-label="Close"><X /></button></header><div className="request-drawer__body"><StatusBadge status={selected.status} language={language} /><dl><div><dt>{t('type')}</dt><dd>{typeLabels[language][selected.request_type]}</dd></div><div><dt>{ru ? 'Контакт' : 'Contact'}</dt><dd><a href={selected.contact.includes('@') ? `mailto:${selected.contact}` : `tel:${selected.contact}`}>{selected.contact}</a></dd></div><div><dt>{ru ? 'Дата и время' : 'Date and time'}</dt><dd>{formatDateTime(selected.desired_datetime, ru ? 'ru-RU' : 'en-GB')}</dd></div>{selected.person_count && <div><dt><Users size={15} /> {ru ? 'Гости' : 'Guests'}</dt><dd>{selected.person_count}</dd></div>}<div><dt>{ru ? 'Создана' : 'Created'}</dt><dd>{formatDateTime(selected.created_at, ru ? 'ru-RU' : 'en-GB')}</dd></div></dl>{selected.comment && <section><h3>{ru ? 'Комментарий' : 'Comment'}</h3><p>{selected.comment}</p></section>}{selected.items.length > 0 && <section><h3>{ru ? 'Состав предзаказа' : 'Pre-order items'}</h3><div className="drawer-items">{selected.items.map((item) => <div key={`${item.menu_item_id}-${item.title}`}><span><b>{item.title}</b><small>{item.quantity} × {formatMoney(item.price_amount, item.price_currency, ru ? 'ru-RU' : 'en-GB')}</small></span><strong>{formatMoney(Number(item.price_amount) * item.quantity, item.price_currency, ru ? 'ru-RU' : 'en-GB')}</strong></div>)}</div></section>}</div><footer>{statusTransitions[selected.status].length === 0 ? <p>{ru ? 'Заявка завершена — статус больше нельзя изменить.' : 'This request is final and cannot be changed.'}</p> : statusTransitions[selected.status].map((next) => <Button key={next} variant={next === 'CANCELLED' ? 'danger' : 'primary'} loading={updatingId === selected.id} onClick={() => void changeStatus(selected, next)}>{next === 'CONFIRMED' ? (ru ? 'Подтвердить' : 'Confirm') : next === 'DONE' ? (ru ? 'Завершить' : 'Complete') : (ru ? 'Отменить' : 'Cancel')}</Button>)}</footer></aside></div>}
    </div>
  );
}
