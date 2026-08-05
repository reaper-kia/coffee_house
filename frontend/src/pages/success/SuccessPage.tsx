import { Check, Clock3 } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../../app/providers/LanguageProvider';
import type { CustomerRequest } from '../../entities/customer-request/model';
import { formatDateTime } from '../../shared/lib/format';

export function SuccessPage() {
  const { state } = useLocation();
  const request = (state as { request?: CustomerRequest } | null)?.request;
  const { language, t } = useLanguage();
  const ru = language === 'ru';
  return (
    <section className="success-page"><div className="success-card"><span className="success-card__icon"><Check /></span><p className="eyebrow eyebrow--dark">NCNL · Received</p><h1>{ru ? 'Заявка отправлена' : 'Request received'}</h1><p>{ru ? 'Администратор свяжется с вами по указанному контакту после подтверждения.' : 'Our manager will contact you using the details provided once it is confirmed.'}</p>{request && <div className="success-summary"><div><span>{ru ? 'Номер заявки' : 'Request reference'}</span><strong>#{request.id.slice(0, 8).toUpperCase()}</strong></div><div><span>{ru ? 'Дата и время' : 'Date and time'}</span><strong><Clock3 size={16} /> {formatDateTime(request.desired_datetime, ru ? 'ru-RU' : 'en-GB')}</strong></div></div>}<div className="success-actions"><Link className="button button--primary" to="/">{t('home')}</Link><Link className="button button--secondary" to="/menu">{t('viewMenu')}</Link></div></div></section>
  );
}
