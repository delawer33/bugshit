import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h2 style={{ margin: "0 0 1.5rem", fontSize: "1.25rem" }}>TaskFlow</h2>
        <nav>
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/tasks">Tasks</NavLink>
          <NavLink to="/projects">Projects</NavLink>
          <NavLink to="/wallet">Wallet</NavLink>
          <NavLink to="/search">Search</NavLink>
          <NavLink to="/settings">Settings</NavLink>
          {user?.is_admin && <NavLink to="/admin">Admin</NavLink>}
        </nav>
        <div style={{ marginTop: "2rem", fontSize: "0.875rem", color: "var(--muted)" }}>
          <div>{user?.display_name}</div>
          <button className="btn-ghost" style={{ marginTop: "0.5rem" }} onClick={logout}>
            Sign out
          </button>
        </div>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
