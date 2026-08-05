import { Clock3, Mail, MapPin, Phone } from 'lucide-react';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { config } from '../../shared/config/env';

export function ContactsPage() {
  const { language } = useLanguage();
  const ru = language === 'ru';
  const mapQuery = encodeURIComponent(config.venue.address);
  return (
    <section className="page-section contact-page"><div className="container"><header className="page-heading"><p className="eyebrow eyebrow--dark">NCNL · Shoreditch</p><h1>{ru ? 'Найдите свой тихий угол в Лондоне.' : 'Find your quiet corner in London.'}</h1><p>{ru ? 'Пять минут от Shoreditch High Street. Заходите без брони или сохраните столик заранее.' : 'Five minutes from Shoreditch High Street. Walk in or reserve a table ahead.'}</p></header><div className="contact-grid"><div className="contact-card"><div><MapPin /><span><small>{ru ? 'Адрес' : 'Address'}</small><strong>{config.venue.address}</strong><a href={`https://www.google.com/maps/search/?api=1&query=${mapQuery}`} target="_blank" rel="noreferrer">{ru ? 'Открыть карту ↗' : 'Open map ↗'}</a></span></div><div><Clock3 /><span><small>{ru ? 'Часы' : 'Hours'}</small><strong>{ru ? 'Пн–Пт 07:30–20:00' : 'Mon–Fri 07:30–20:00'}</strong><strong>{ru ? 'Сб–Вс 08:00–20:00' : 'Sat–Sun 08:00–20:00'}</strong></span></div><div><Phone /><span><small>{ru ? 'Телефон' : 'Phone'}</small><a href={`tel:${config.venue.phone.replace(/\s/g, '')}`}>{config.venue.phone}</a></span></div><div><Mail /><span><small>Email</small><a href={`mailto:${config.venue.email}`}>{config.venue.email}</a></span></div></div><div className="contact-map"><div className="contact-map__streets"><span className="street street--one">Bethnal Green Rd</span><span className="street street--two">Redchurch St</span><span className="street street--three">Brick Lane</span><span className="map-pin"><MapPin /><b>NCNL</b></span></div></div></div></div></section>
  );
}
