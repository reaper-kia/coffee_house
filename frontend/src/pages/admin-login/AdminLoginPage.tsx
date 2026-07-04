import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../../shared/ui/Input';
import { Button } from '../../shared/ui/Button';
import { config } from '../../shared/config/env';

export const AdminLoginPage = () => {
  const navigate = useNavigate();
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginCode, setLoginCode] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      if (config.USE_MOCK_API) {
        await new Promise((resolve) => setTimeout(resolve, 500));
        
        if (loginCode !== 'admin_penis') {
          throw new Error('Неверный секретный код!');
        }
        
        if (!username.trim() || !password.trim()) {
          throw new Error('Введите логин и пароль');
        }
        
        if (password.length < 6) {
          throw new Error('Пароль должен содержать минимум 6 символов');
        }
        
        // Читаем данные из localStorage
        const usersJson = localStorage.getItem('mock_users');
        console.log('Данные из localStorage:', usersJson);
        
        // ВАЖНО: Проверяем, что это объект, а не массив
        let users: Record<string, { password: string; createdAt: string }> = {};
        if (usersJson) {
          try {
            const parsed = JSON.parse(usersJson);
            // Если это массив — игнорируем и начинаем с пустого объекта
            if (Array.isArray(parsed)) {
              console.warn('⚠️ Найдены старые данные в формате массива, игнорируем');
              localStorage.removeItem('mock_users');
            } else {
              users = parsed;
            }
          } catch (parseError) {
            console.error('Ошибка парсинга:', parseError);
          }
        }
        
        console.log('Текущие пользователи:', users);
        
        if (isRegister) {
          if (users[username]) {
            throw new Error('Пользователь с таким логином уже существует');
          }
          
          users[username] = { 
            password: password, 
            createdAt: new Date().toISOString() 
          };
          
          localStorage.setItem('mock_users', JSON.stringify(users));
          console.log('✅ Пользователь сохранен:', users);
          
          alert(`Регистрация успешна!\nЛогин: ${username}\nПароль: ${password}`);
          
        } else {
          console.log('Попытка входа как:', username);
          
          if (!users[username]) {
            throw new Error(`Пользователь "${username}" не найден. Сначала зарегистрируйтесь`);
          }
          
          if (users[username].password !== password) {
            throw new Error('Неверный пароль');
          }
          
          console.log('✅ Вход успешен');
        }
        
        localStorage.setItem('access_token', `mock-token-${username}-${Date.now()}`);
        localStorage.setItem('current_user', username);
        navigate('/admin/requests');
        
      } else {
        const endpoint = isRegister ? '/auth/register' : '/auth/login';
        const response = await fetch(`${config.API_BASE_URL}${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username,
            password,
            login_code: loginCode,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.message || 'Ошибка запроса');
        }

        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('current_user', username);
        navigate('/admin/requests');
      }
    } catch (err) {
      console.error('Ошибка:', err);
      setError(err instanceof Error ? err.message : 'Ошибка');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '40px auto', padding: '20px' }}>
      <h1>{isRegister ? '🔐 Регистрация админа' : '🔐 Вход в админку'}</h1>
      <form onSubmit={handleSubmit}>
        <Input
          label="Секретный код"
          value={loginCode}
          onChange={(e) => setLoginCode(e.target.value)}
          placeholder="Код от тимлида"
        />
        <Input
          label="Логин"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          label="Пароль"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>}
        <Button type="submit" disabled={isLoading} style={{ width: '100%' }}>
          {isLoading ? 'Загрузка...' : (isRegister ? 'Зарегистрироваться' : 'Войти')}
        </Button>
      </form>
      
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <button
          onClick={() => {
            setIsRegister(!isRegister);
            setError(null);
          }}
          style={{
            background: 'none',
            border: 'none',
            color: '#007bff',
            cursor: 'pointer',
            textDecoration: 'underline',
            fontSize: '14px',
          }}
        >
          {isRegister ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрироваться'}
        </button>
      </div>
    </div>
  );
};