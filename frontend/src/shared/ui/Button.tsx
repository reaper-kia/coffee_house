import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

export const Button = ({ variant = 'primary', style, ...props }: ButtonProps) => {
  const baseStyle: React.CSSProperties = {
    padding: '10px 20px',
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
    ...style,
  };

  const variants = {
    primary: { background: '#007bff', color: 'white' },
    secondary: { background: '#6c757d', color: 'white' },
  };

  return <button style={{ ...baseStyle, ...variants[variant] }} {...props} />;
};