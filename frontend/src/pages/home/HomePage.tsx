import { Link } from 'react-router-dom';

export const HomePage = () => (
  <div style={{ padding: 20 }}>
    <h1>🍽 Добро пожаловать!</h1>
    <nav style={{ display: 'flex', gap: 16, marginTop: 20 }}>
      <Link to="/menu">Меню</Link>
      <Link to="/booking">Бронь столика</Link>
      <Link to="/preorder">Предзаказ</Link>
      <Link to="/admin/requests">Админка</Link>
    </nav>
  </div>
);