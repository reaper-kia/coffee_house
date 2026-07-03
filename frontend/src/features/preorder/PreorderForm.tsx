import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../../shared/ui/Input';
import { Textarea } from '../../shared/ui/Textarea';
import { Button } from '../../shared/ui/Button';
import { Loading } from '../../shared/ui/Loading';
import { catalogApi } from '../../entities/catalog/api';
import { customerRequestApi } from '../../entities/customer-request/api';
import { MenuItem } from '../../entities/catalog/types';
import { validatePreorder, PreorderFormValues, PreorderErrors } from './preorderValidation';
import { SelectedPreorderItems } from './SelectedPreorderItems';

export const PreorderForm = () => {
  const navigate = useNavigate();
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [values, setValues] = useState<PreorderFormValues>({
    name: '', phone: '', pickupDate: '', pickupTime: '', items: [], comment: '',
  });
  const [errors, setErrors] = useState<PreorderErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    catalogApi.getMenu().then((data) => {
      setMenu(data);
      setLoading(false);
    });
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof PreorderErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleItemChange = (menuItemId: string, checked: boolean) => {
    setValues((prev) => {
      if (checked) {
        return { ...prev, items: [...prev.items, { menuItemId, quantity: 1 }] };
      } else {
        return { ...prev, items: prev.items.filter((i) => i.menuItemId !== menuItemId) };
      }
    });
  };

  const handleQuantityChange = (menuItemId: string, quantity: number) => {
    setValues((prev) => ({
      ...prev,
      items: prev.items.map((i) => (i.menuItemId === menuItemId ? { ...i, quantity } : i)),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const validationErrors = validatePreorder(values);
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length === 0) {
      setIsSubmitting(true);
      try {
        await customerRequestApi.createPreorder(values);
        navigate('/success');
      } catch (error) {
        console.error('Ошибка при создании предзаказа:', error);
        alert('Ошибка при создании предзаказа.');
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  if (loading) return <Loading />;

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2>Оформить предзаказ</h2>
      
      <h3>1. Ваши данные</h3>
      <Input label="Ваше имя" name="name" value={values.name} onChange={handleChange} error={errors.name} />
      <Input label="Телефон" name="phone" value={values.phone} onChange={handleChange} error={errors.phone} />
      <Input label="Дата получения" name="pickupDate" type="date" value={values.pickupDate} onChange={handleChange} error={errors.pickupDate} />
      <Input label="Время получения" name="pickupTime" type="time" value={values.pickupTime} onChange={handleChange} error={errors.pickupTime} />
      <Textarea label="Комментарий" name="comment" value={values.comment} onChange={handleChange} />

      <h3>2. Выберите блюда</h3>
      {errors.items && <p style={{ color: 'red' }}>{errors.items}</p>}
      <div style={{ marginBottom: '20px' }}>
        {menu.map((item) => {
          const isSelected = values.items.some((i) => i.menuItemId === item.id);
          const quantity = values.items.find((i) => i.menuItemId === item.id)?.quantity || 1;
          return (
            <div key={item.id} style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px', padding: '10px', border: '1px solid #eee', borderRadius: '8px' }}>
              <input type="checkbox" checked={isSelected} onChange={(e) => handleItemChange(item.id, e.target.checked)} />
              <span style={{ flex: 1 }}><b>{item.name}</b> - {item.price} руб.</span>
              {isSelected && (
                <input 
                  type="number" 
                  min="1" 
                  max="10" 
                  value={quantity} 
                  onChange={(e) => handleQuantityChange(item.id, Number(e.target.value))}
                  style={{ width: '60px', padding: '5px' }}
                />
              )}
            </div>
          );
        })}
      </div>

      <h3>3. Итого</h3>
      <SelectedPreorderItems menu={menu} selectedItems={values.items} />

      <Button type="submit" disabled={isSubmitting} style={{ width: '100%' }}>
        {isSubmitting ? 'Оформляем...' : 'Оформить предзаказ'}
      </Button>
    </form>
  );
};