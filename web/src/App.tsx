import { CircularProgress, Stack } from '@mui/material';
import { Navigate, Route, Routes } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { AppShell } from './layouts/AppShell';
import { AttendancePage } from './pages/AttendancePage';
import { DashboardPage } from './pages/DashboardPage';
import { DisciplinesPage } from './pages/DisciplinesPage';
import { EnrollmentsPage } from './pages/EnrollmentsPage';
import { FirstAccessPage } from './pages/FirstAccessPage';
import { ForgotPasswordPage } from './pages/ForgotPasswordPage';
import { HomePage } from './pages/HomePage';
import { InstitutionsPage } from './pages/InstitutionsPage';
import { LoginPage } from './pages/LoginPage';
import { StudentsPage } from './pages/StudentsPage';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) {
    return (
      <Stack alignItems="center" justifyContent="center" sx={{ minHeight: '100vh' }}>
        <CircularProgress />
      </Stack>
    );
  }
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/first-access" element={<FirstAccessPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/app" element={<ProtectedRoute><AppShell><DashboardPage /></AppShell></ProtectedRoute>} />
      <Route path="/app/institutions" element={<ProtectedRoute><AppShell><InstitutionsPage /></AppShell></ProtectedRoute>} />
      <Route path="/app/disciplines" element={<ProtectedRoute><AppShell><DisciplinesPage /></AppShell></ProtectedRoute>} />
      <Route path="/app/students" element={<ProtectedRoute><AppShell><StudentsPage /></AppShell></ProtectedRoute>} />
      <Route path="/app/enrollments" element={<ProtectedRoute><AppShell><EnrollmentsPage /></AppShell></ProtectedRoute>} />
      <Route path="/app/attendance" element={<ProtectedRoute><AppShell><AttendancePage /></AppShell></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
