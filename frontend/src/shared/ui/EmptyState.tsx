export const EmptyState = ({ message }: { message: string }) => (
  <div
    style={{
      textAlign: 'center',
      padding: '40px 20px',
      color: '#999',
      fontSize: '16px',
    }}
  >
    📭 {message}
  </div>
);