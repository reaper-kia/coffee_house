import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HomePage } from '../pages/home/HomePage';
import { MenuPage } from '../pages/menu/MenuPage';
import { BookingPage } from '../pages/booking/BookingPage';
import { PreorderPage } from '../pages/preorder/PreorderPage';
import { SuccessPage } from '../pages/success/SuccessPage';
import { AdminLoginPage } from '../pages/admin-login/AdminLoginPage';
import { AdminRequestsPage } from '../pages/admin/AdminRequestsPage';

export const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/menu" element={<MenuPage />} />
      <Route path="/booking" element={<BookingPage />} />
      <Route path="/preorder" element={<PreorderPage />} />
      <Route path="/success" element={<SuccessPage />} />
      <Route path="/admin/login" element={<AdminLoginPage />} />
      <Route path="/admin/requests" element={<AdminRequestsPage />} />
    </Routes>
  </BrowserRouter>
);