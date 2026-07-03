import { Link } from 'react-router-dom';
export const SuccessPage = () => (
  <div style={{ padding: 20 }}>
    <h1>Заявка отправлена</h1>
    <p>Администратор свяжется с вами для подтверждения.</p>
    <Link to="/">← На главную</Link>
  </div>
);