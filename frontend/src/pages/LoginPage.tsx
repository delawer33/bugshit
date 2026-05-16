import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login, error } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      await login(username, password);
      navigate("/");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-page">
      <h1>Sign in to TaskFlow</h1>
      <form className="card" onSubmit={onSubmit}>
        {error && <p className="error-text">{error}</p>}
        <div className="form-group">
          <label>Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button className="btn" type="submit" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
      <p>
        No account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}
