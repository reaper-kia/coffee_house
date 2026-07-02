import { TextareaHTMLAttributes } from 'react';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const Textarea = ({ label, error, style, ...props }: TextareaProps) => (
  <div style={{ marginBottom: '15px' }}>
    {label && <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>{label}</label>}
    <textarea
      style={{
        width: '100%',
        padding: '10px',
        borderRadius: '8px',
        border: error ? '1px solid red' : '1px solid #ccc',
        minHeight: '100px',
        boxSizing: 'border-box',
        ...style,
      }}
      {...props}
    />
    {error && <span style={{ color: 'red', fontSize: '12px', marginTop: '5px', display: 'block' }}>{error}</span>}
  </div>
);