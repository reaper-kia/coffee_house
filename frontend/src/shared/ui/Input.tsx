import { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = ({ label, error, style, ...props }: InputProps) => (
  <div style={{ marginBottom: '15px' }}>
    {label && <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>{label}</label>}
    <input
      style={{
        width: '100%',
        padding: '10px',
        borderRadius: '8px',
        border: error ? '1px solid red' : '1px solid #ccc',
        boxSizing: 'border-box',
        ...style,
      }}
      {...props}
    />
    {error && <span style={{ color: 'red', fontSize: '12px', marginTop: '5px', display: 'block' }}>{error}</span>}
  </div>
);