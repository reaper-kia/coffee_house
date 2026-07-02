import { Link } from 'react-router-dom';
export const SuccessPage = () => (
  <div style={{ padding: 20 }}>
    <h1>✅ Заявка принята!</h1>
    <Link to="/">← На главную</Link>
  </div>
);