import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api';
import type { User } from '../types';

interface AuthContextValue {
  token: string;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string>(() => localStorage.getItem('attend_token') || '');
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(!!token);

  useEffect(() => {
    async function loadMe() {
      if (!token) {
        setIsLoading(false);
        setUser(null);
        return;
      }
      try {
        const me = await apiRequest<User>('/auth/me', {}, token);
        setUser(me);
      } catch {
        localStorage.removeItem('attend_token');
        setToken('');
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }
    loadMe();
  }, [token]);

  async function login(username: string, password: string) {
    const data = await apiRequest<{ access_token: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    localStorage.setItem('attend_token', data.access_token);
    setToken(data.access_token);
    setIsLoading(true);
  }

  function logout() {
    localStorage.removeItem('attend_token');
    setToken('');
    setUser(null);
    setIsLoading(false);
  }

  const value = useMemo(() => ({
    token,
    user,
    isAuthenticated: !!token && !!user,
    isLoading,
    login,
    logout,
  }), [token, user, isLoading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
