import { Link } from 'react-router-dom';
import { useLanguage } from '../../app/providers/LanguageProvider';

export function NotFoundPage() {
  const { language, t } = useLanguage();
  return <section className="not-found"><span>404</span><h1>{language === 'ru' ? 'Эта страница остыла' : 'This page has gone cold'}</h1><p>{language === 'ru' ? 'Вернёмся туда, где кофе ещё горячий.' : 'Let’s head back to where the coffee is still hot.'}</p><Link className="button button--primary" to="/">{t('home')}</Link></section>;
}
