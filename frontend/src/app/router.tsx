import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ProtectedRoute } from '../features/auth/ProtectedRoute';
import { AdminLoginPage } from '../pages/admin-login/AdminLoginPage';
import { AdminRequestsPage } from '../pages/admin/AdminRequestsPage';
import { BookingPage } from '../pages/booking/BookingPage';
import { ContactsPage } from '../pages/contacts/ContactsPage';
import { EventsPage } from '../pages/events/EventsPage';
import { HomePage } from '../pages/home/HomePage';
import { MenuPage } from '../pages/menu/MenuPage';
import { NotFoundPage } from '../pages/not-found/NotFoundPage';
import { PreorderPage } from '../pages/preorder/PreorderPage';
import { SuccessPage } from '../pages/success/SuccessPage';
import { PublicLayout } from '../widgets/layout/PublicLayout';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/menu" element={<MenuPage />} />
          <Route path="/booking" element={<BookingPage />} />
          <Route path="/preorder" element={<PreorderPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/contacts" element={<ContactsPage />} />
          <Route path="/success" element={<SuccessPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
        <Route path="/admin/login" element={<AdminLoginPage />} />
        <Route path="/admin" element={<Navigate to="/admin/requests" replace />} />
        <Route path="/admin/requests" element={<ProtectedRoute><AdminRequestsPage /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  );
}
