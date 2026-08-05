import { useEffect, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import { Coffee, Menu, Moon, ShoppingBag, Sun, X } from 'lucide-react';
import { useCart } from '../../app/providers/CartProvider';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { useTheme } from '../../app/providers/ThemeProvider';
import { config } from '../../shared/config/env';

export function PublicLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { language, setLanguage, t } = useLanguage();
  const { theme, toggleTheme } = useTheme();
  const { itemCount } = useCart();
  const location = useLocation();

  useEffect(() => {
    setMobileOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [location.pathname]);

  const nav = [
    ['/', t('home')], ['/menu', t('menu')], ['/booking', t('booking')],
    ['/events', t('events')], ['/contacts', t('contacts')],
  ];

  return (
    <div className="site-shell">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <header className="site-header">
        <div className="container site-header__inner">
          <Link to="/" className="brand" aria-label="NCNL Coffee, home">
            <span className="brand__mark">NCNL</span><span className="brand__caption">Coffee · London</span>
          </Link>
          <nav className={mobileOpen ? 'site-nav site-nav--open' : 'site-nav'} aria-label="Main navigation">
            {nav.map(([path, label]) => (
              <NavLink key={path} to={path} end={path === '/'} className={({ isActive }) => isActive ? 'active' : ''}>{label}</NavLink>
            ))}
            <NavLink to="/preorder" className={({ isActive }) => `site-nav__cart ${isActive ? 'active' : ''}`}>
              <ShoppingBag size={18} />{t('cart')}{itemCount > 0 && <span>{itemCount}</span>}
            </NavLink>
          </nav>
          <div className="site-header__tools">
            <button className="icon-button language-toggle" type="button" onClick={() => setLanguage(language === 'ru' ? 'en' : 'ru')} aria-label="Change language">
              {language === 'ru' ? 'EN' : 'RU'}
            </button>
            <button className="icon-button" type="button" onClick={toggleTheme} aria-label="Change theme">
              {theme === 'light' ? <Moon size={19} /> : <Sun size={19} />}
            </button>
            <button className="icon-button mobile-toggle" type="button" onClick={() => setMobileOpen((value) => !value)} aria-label="Menu" aria-expanded={mobileOpen}>
              {mobileOpen ? <X size={21} /> : <Menu size={21} />}
            </button>
          </div>
        </div>
      </header>
      <main id="main-content"><Outlet /></main>
      <footer className="site-footer">
        <div className="container site-footer__grid">
          <div><div className="brand brand--footer"><span className="brand__mark">NCNL</span><span className="brand__caption">Coffee · London</span></div><p>{language === 'ru' ? 'Независимая кофейня в сердце Шордича.' : 'An independent coffee house in the heart of Shoreditch.'}</p></div>
          <div><h3>{language === 'ru' ? 'Приходите' : 'Visit'}</h3><address>{config.venue.address}</address><a href={`tel:${config.venue.phone.replace(/\s/g, '')}`}>{config.venue.phone}</a></div>
          <div><h3>{language === 'ru' ? 'Часы работы' : 'Opening hours'}</h3><p>{language === 'ru' ? 'Пн–Пт 07:30–20:00' : 'Mon–Fri 07:30–20:00'}<br />{language === 'ru' ? 'Сб–Вс 08:00–20:00' : 'Sat–Sun 08:00–20:00'}</p></div>
          <div><h3>{language === 'ru' ? 'Для команды' : 'Team'}</h3><Link to="/admin/login"><Coffee size={16} /> {t('admin')}</Link></div>
        </div>
        <div className="container site-footer__bottom">© {new Date().getFullYear()} NCNL Coffee</div>
      </footer>
    </div>
  );
}
