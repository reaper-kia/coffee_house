import { ArrowRight, CalendarDays, Coffee, MapPin, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../../app/providers/LanguageProvider';

export function HomePage() {
  const { language, t } = useLanguage();
  const ru = language === 'ru';
  return (
    <>
      <section className="hero">
        <div className="hero__image" role="img" aria-label="NCNL Coffee interior in London" />
        <div className="hero__overlay" />
        <div className="container hero__content">
          <span className="eyebrow"><MapPin size={15} /> Shoreditch · London</span>
          <h1>{ru ? <>Кофе, ради которого<br />стоит замедлиться.</> : <>Coffee worth<br />slowing down for.</>}</h1>
          <p>{ru ? 'Свежеобжаренное зерно, сезонная кухня и спокойное место посреди Лондона.' : 'Freshly roasted coffee, a seasonal kitchen and a calm corner in the middle of London.'}</p>
          <div className="hero__actions">
            <Link to="/booking" className="button button--primary">{t('bookTable')} <ArrowRight size={18} /></Link>
            <Link to="/menu" className="button button--on-dark">{t('viewMenu')}</Link>
          </div>
        </div>
        <div className="hero__note"><span>{ru ? 'Сегодня' : 'Today'}</span><strong>07:30 — 20:00</strong></div>
      </section>

      <section className="section section--intro">
        <div className="container intro-grid">
          <div><span className="section-number">01</span><p className="eyebrow eyebrow--dark">NCNL Coffee House</p><h2>{ru ? 'Простое, сделанное без компромиссов.' : 'Simple things, made without compromise.'}</h2></div>
          <div className="intro-grid__copy"><p>{ru ? 'Мы работаем с небольшими обжарщиками, меняем зерно по сезону и готовим всё на открытой кухне каждое утро.' : 'We work with independent roasters, change our beans with the seasons and prepare everything in our open kitchen each morning.'}</p><p>{ru ? 'NCNL — это место для неспешного завтрака, рабочего эспрессо и длинного разговора за общим столом.' : 'NCNL is a place for a slow breakfast, a working espresso and a long conversation around the communal table.'}</p><Link to="/menu" className="text-link">{t('viewMenu')} <ArrowRight size={16} /></Link></div>
        </div>
      </section>

      <section className="section section--features">
        <div className="container feature-grid">
          <article className="feature-card"><span><Coffee /></span><h3>{ru ? 'Specialty coffee' : 'Specialty coffee'}</h3><p>{ru ? 'Точно настроенный эспрессо и фильтр, который меняется каждую неделю.' : 'Dialled-in espresso and a weekly rotating filter.'}</p></article>
          <article className="feature-card"><span><Sparkles /></span><h3>{ru ? 'Своя выпечка' : 'Baked in house'}</h3><p>{ru ? 'Круассаны, тарты и сезонные десерты из нашей утренней выпечки.' : 'Croissants, tarts and seasonal sweets from our morning bake.'}</p></article>
          <article className="feature-card"><span><CalendarDays /></span><h3>{ru ? 'Ваши события' : 'Your occasions'}</h3><p>{ru ? 'Камерные ужины, встречи команд и маленькие праздники до 60 гостей.' : 'Intimate dinners, team gatherings and small celebrations for up to 60 guests.'}</p></article>
        </div>
      </section>

      <section className="section story-split">
        <div className="story-split__image"><img src="/images/ncnl-coffee.webp" alt="Flat white in a ceramic cup" /></div>
        <div className="story-split__content"><span className="section-number">02</span><p className="eyebrow eyebrow--dark">{ru ? 'Наша чашка' : 'In every cup'}</p><h2>{ru ? 'Знакомый вкус. Новый характер.' : 'Familiar comfort. A new character.'}</h2><p>{ru ? 'От сладкого бразильского эспрессо до яркой Эфиопии в фильтре — бариста помогут найти именно ваш кофе.' : 'From sweet Brazilian espresso to a bright Ethiopian filter, our baristas will help you find your coffee.'}</p><Link to="/menu" className="button button--secondary">{t('viewMenu')}</Link></div>
      </section>

      <section className="section section--cta">
        <div className="container cta-card"><div><p className="eyebrow">{ru ? 'Ваш стол ждёт' : 'Your table is waiting'}</p><h2>{ru ? 'Встретимся в Шордиче?' : 'Meet us in Shoreditch?'}</h2></div><Link to="/booking" className="button button--light">{t('bookTable')} <ArrowRight size={18} /></Link></div>
      </section>
    </>
  );
}
