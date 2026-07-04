import { Navigate } from 'react-router-dom';

export const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }
  
  return <>{children}</>;
};