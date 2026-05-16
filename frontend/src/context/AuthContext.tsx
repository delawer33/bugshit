import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { clearToken, getToken } from "../api/client";
import { login as apiLogin, register as apiRegister } from "../api/auth";
import { fetchMe } from "../api/users";
import type { User } from "../types";

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!getToken()) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const me = await fetchMe();
      setUser(me);
      setError(null);
    } catch (e) {
      setUser(null);
      clearToken();
      setError(e instanceof Error ? e.message : "Session expired");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const login = useCallback(async (username: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      await apiLogin(username, password);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Login failed");
      throw e;
    } finally {
      setLoading(false);
    }
  }, [refresh]);

  const register = useCallback(
    async (email: string, username: string, password: string) => {
      setLoading(true);
      setError(null);
      try {
        await apiRegister(email, username, password);
        await apiLogin(username, password);
        await refresh();
      } catch (e) {
        setError(e instanceof Error ? e.message : "Registration failed");
        throw e;
      } finally {
        setLoading(false);
      }
    },
    [refresh]
  );

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, loading, error, login, register, logout, refresh }),
    [user, loading, error, login, register, logout, refresh]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
