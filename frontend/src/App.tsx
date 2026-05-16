import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import { AuthProvider, useAuth } from "./context/AuthContext";
import AdminPage from "./pages/AdminPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import ProjectsPage from "./pages/ProjectsPage";
import RegisterPage from "./pages/RegisterPage";
import SearchPage from "./pages/SearchPage";
import SettingsPage from "./pages/SettingsPage";
import TaskDetailPage from "./pages/TaskDetailPage";
import TasksPage from "./pages/TasksPage";
import WalletPage from "./pages/WalletPage";

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <p>Loading…</p>;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="tasks" element={<TasksPage />} />
        <Route path="tasks/:id" element={<TaskDetailPage />} />
        <Route path="projects" element={<ProjectsPage />} />
        <Route path="wallet" element={<WalletPage />} />
        <Route path="search" element={<SearchPage />} />
        <Route path="settings" element={<SettingsPage />} />
        <Route path="admin" element={<AdminPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
