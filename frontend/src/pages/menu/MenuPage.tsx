import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Check, Plus, Search, ShoppingBag, X } from 'lucide-react';
import { catalogApi } from '../../entities/catalog/api';
import type { MenuCategory, MenuItem } from '../../entities/catalog/types';
import { useCart } from '../../app/providers/CartProvider';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { useToast } from '../../app/providers/ToastProvider';
import { config } from '../../shared/config/env';
import { formatMoney } from '../../shared/lib/format';
import { Button } from '../../shared/ui/Button';
import { EmptyState } from '../../shared/ui/EmptyState';
import { ErrorMessage } from '../../shared/ui/ErrorMessage';
import { Loading } from '../../shared/ui/Loading';

function fallbackImage(item: MenuItem) {
  const text = `${item.category_title ?? ''} ${item.title}`.toLowerCase();
  return /coffee|коф|drink|напит|tea|чай|latte|espresso/.test(text)
    ? '/images/ncnl-coffee.webp'
    : '/images/ncnl-pastry.webp';
}

export function MenuPage() {
  const { language, t } = useLanguage();
  const { add, lines } = useCart();
  const { showToast } = useToast();
  const [categories, setCategories] = useState<MenuCategory[]>([]);
  const [items, setItems] = useState<MenuItem[]>([]);
  const [categoryId, setCategoryId] = useState('');
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [selected, setSelected] = useState<MenuItem | null>(null);
  const requestId = useRef(0);
  const ru = language === 'ru';

  useEffect(() => {
    catalogApi.getCategories().then(setCategories).catch(() => setCategories([]));
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedSearch(search), 300);
    return () => window.clearTimeout(timer);
  }, [search]);

  const fetchItems = useCallback(async (offset: number, reset: boolean) => {
    const id = ++requestId.current;
    if (reset) setLoading(true);
    else setLoadingMore(true);
    setError(null);
    try {
      const result = await catalogApi.getMenuItems({
        categoryId: categoryId || undefined,
        search: debouncedSearch || undefined,
        limit: config.menuPageSize,
        offset,
      });
      if (id !== requestId.current) return;
      setItems((current) => reset ? result : [...current, ...result]);
      setHasMore(result.length === config.menuPageSize);
    } catch (err) {
      if (id === requestId.current) setError(err instanceof Error ? err.message : 'Menu request failed');
    } finally {
      if (id === requestId.current) { setLoading(false); setLoadingMore(false); }
    }
  }, [categoryId, debouncedSearch]);

  useEffect(() => { void fetchItems(0, true); }, [fetchItems]);

  const cartIds = useMemo(() => new Set(lines.map((line) => line.item.id)), [lines]);
  const handleAdd = (item: MenuItem) => {
    add(item);
    showToast(ru ? `${item.title} добавлен в корзину` : `${item.title} added to basket`);
  };

  return (
    <section className="page-section menu-page">
      <div className="container">
        <header className="page-heading page-heading--split"><div><p className="eyebrow eyebrow--dark">NCNL · Seasonal</p><h1>{ru ? 'Меню' : 'Menu'}</h1><p>{ru ? 'Завтраки весь день, выпечка из нашей кухни и кофе от независимых обжарщиков.' : 'All-day breakfast, pastries from our kitchen and coffee from independent roasters.'}</p></div><img src="/images/ncnl-pastry.webp" alt="Fresh pastry selection" /></header>
        <div className="menu-toolbar">
          <div className="category-tabs" role="tablist" aria-label="Menu categories">
            <button className={!categoryId ? 'active' : ''} onClick={() => setCategoryId('')}>{t('allCategories')}</button>
            {categories.map((category) => <button key={category.id} className={categoryId === category.id ? 'active' : ''} onClick={() => setCategoryId(category.id)}>{category.title}</button>)}
          </div>
          <label className="search-field"><Search size={18} /><input type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder={t('search')} aria-label={t('search')} />{search && <button type="button" onClick={() => setSearch('')} aria-label="Clear"><X size={16} /></button>}</label>
        </div>

        {loading && <Loading label={t('loading')} />}
        {!loading && error && <ErrorMessage message={error} onRetry={() => void fetchItems(0, true)} retryLabel={t('retry')} />}
        {!loading && !error && items.length === 0 && <EmptyState title={ru ? 'Ничего не найдено' : 'Nothing found'} message={ru ? 'Попробуйте другую категорию или запрос.' : 'Try another category or search.'} />}
        {!loading && !error && items.length > 0 && (
          <div className="menu-grid">
            {items.map((item) => (
              <article className="menu-card" key={item.id}>
                <button className="menu-card__image" type="button" onClick={() => setSelected(item)} aria-label={`${t('details')}: ${item.title}`}><img src={item.image_url || fallbackImage(item)} onError={(event) => { event.currentTarget.src = fallbackImage(item); }} alt={item.title} loading="lazy" /><span>{item.category_title ?? (ru ? 'Сезонное' : 'Seasonal')}</span></button>
                <div className="menu-card__body"><div><h2>{item.title}</h2><p>{item.description || (ru ? 'Уточните детали у бариста.' : 'Ask our barista for today’s details.')}</p></div><div className="menu-card__footer"><strong>{formatMoney(item.price_amount, item.price_currency, ru ? 'ru-RU' : 'en-GB')}</strong><Button type="button" variant="ghost" onClick={() => handleAdd(item)} aria-label={`${t('add')}: ${item.title}`}>{cartIds.has(item.id) ? <Check size={17} /> : <Plus size={17} />} {t('add')}</Button></div></div>
              </article>
            ))}
          </div>
        )}
        {hasMore && !loading && <div className="load-more"><Button type="button" variant="secondary" loading={loadingMore} onClick={() => void fetchItems(items.length, false)}>{t('loadMore')}</Button></div>}
      </div>

      {selected && <div className="modal-backdrop" onMouseDown={() => setSelected(null)}><div className="menu-modal" role="dialog" aria-modal="true" aria-labelledby="menu-modal-title" onMouseDown={(event) => event.stopPropagation()}><button type="button" className="modal-close" onClick={() => setSelected(null)} aria-label="Close"><X /></button><img src={selected.image_url || fallbackImage(selected)} onError={(event) => { event.currentTarget.src = fallbackImage(selected); }} alt="" /><div className="menu-modal__content"><p className="eyebrow eyebrow--dark">{selected.category_title}</p><h2 id="menu-modal-title">{selected.title}</h2><p>{selected.description}</p><div><strong>{formatMoney(selected.price_amount, selected.price_currency, ru ? 'ru-RU' : 'en-GB')}</strong><Button onClick={() => { handleAdd(selected); setSelected(null); }}><ShoppingBag size={18} /> {t('add')}</Button></div></div></div></div>}
    </section>
  );
}
