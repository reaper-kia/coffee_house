import { SelectHTMLAttributes } from 'react';

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
}

export const Select = ({ label, options, style, ...props }: SelectProps) => (
  <div style={{ marginBottom: '10px' }}>
    {label && <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>{label}</label>}
    <select
      style={{
        padding: '8px 12px',
        borderRadius: '6px',
        border: '1px solid #ccc',
        fontSize: '14px',
        cursor: 'pointer',
        ...style,
      }}
      {...props}
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  </div>
);