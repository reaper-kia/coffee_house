import { useEffect, useState, type FormEvent } from 'react';
import { ArrowLeft, LockKeyhole } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../../app/providers/LanguageProvider';
import { ApiError } from '../../shared/api/client';
import { Button } from '../../shared/ui/Button';
import { Input } from '../../shared/ui/Input';
import { authApi } from '../../features/auth/api';

export function AdminLoginPage() {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const ru = language === 'ru';
  const [registerMode, setRegisterMode] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [adminCode, setAdminCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    authApi.me().then((user) => { if (user.is_admin) navigate('/admin/requests', { replace: true }); }).catch(() => undefined);
  }, [navigate]);

  const submit = async (event: FormEvent) => {
    event.preventDefault(); setError('');
    if (!email.trim() || password.length < 8 || (registerMode && (!name.trim() || !adminCode.trim()))) {
      setError(ru ? 'Заполните все поля. Пароль — не короче 8 символов.' : 'Complete every field. Password must contain at least 8 characters.');
      return;
    }
    setLoading(true);
    try {
      if (registerMode) {
        const created = await authApi.registerAdmin({
          name: name.trim(), email: email.trim(), password, admin_code: adminCode.trim(),
        });
        if (!created.is_admin) {
          throw new Error(ru
            ? 'Пользователь создан без прав администратора: проверьте admin-код у тимлида.'
            : 'The user was created without admin access. Check the admin code with your team lead.');
        }
      }
      await authApi.login(email.trim(), password);
      const user = await authApi.me();
      if (!user.is_admin) { await authApi.logout(); throw new Error(ru ? 'У этого пользователя нет прав администратора.' : 'This user does not have admin access.'); }
      navigate('/admin/requests', { replace: true });
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) setError(ru ? 'Неверный email или пароль.' : 'Incorrect email or password.');
      else if (err instanceof ApiError && err.status === 409) setError(ru ? 'Пользователь с таким email уже существует.' : 'A user with this email already exists.');
      else setError(err instanceof Error ? err.message : 'Login failed');
    } finally { setLoading(false); }
  };

  return (
    <main className="login-page"><div className="login-page__visual"><Link to="/"><ArrowLeft /> {ru ? 'Вернуться в кофейню' : 'Back to coffee house'}</Link><div><span className="brand__mark">NCNL</span><p>{ru ? 'Служебный вход для команды кофейни.' : 'Team access for the coffee house.'}</p></div></div><div className="login-page__form"><form onSubmit={submit} noValidate><span className="login-icon"><LockKeyhole /></span><p className="eyebrow eyebrow--dark">NCNL · Team</p><h1>{registerMode ? (ru ? 'Регистрация админа' : 'Admin registration') : (ru ? 'Вход в админку' : 'Admin sign in')}</h1><p>{registerMode ? (ru ? 'Admin-код выдаёт тимлид. Он отправляется только backend и не сохраняется в браузере.' : 'Your team lead provides the admin code. It is sent only to the backend and is never stored in the browser.') : (ru ? 'Используйте учётную запись администратора.' : 'Use an administrator account.')}</p>{registerMode && <Input label={ru ? 'Имя' : 'Name'} value={name} onChange={(event) => setName(event.target.value)} autoComplete="name" required />}<Input label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="email" required /><Input label={ru ? 'Пароль' : 'Password'} type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete={registerMode ? 'new-password' : 'current-password'} minLength={8} required />{registerMode && <Input label="Admin code" type="password" value={adminCode} onChange={(event) => setAdminCode(event.target.value)} autoComplete="off" required />}{error && <p className="form-error" role="alert">{error}</p>}<Button type="submit" loading={loading}>{registerMode ? (ru ? 'Создать администратора' : 'Create administrator') : (ru ? 'Войти' : 'Sign in')}</Button><button className="login-mode-toggle" type="button" onClick={() => { setRegisterMode((value) => !value); setError(''); setAdminCode(''); }}>{registerMode ? (ru ? 'Уже есть аккаунт? Войти' : 'Already have an account? Sign in') : (ru ? 'Зарегистрировать администратора' : 'Register an administrator')}</button></form></div></main>
  );
}
