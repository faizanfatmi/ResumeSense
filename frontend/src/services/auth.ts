import api from './api';
import { AuthResponse, User } from '../types';

export const authService = {
  async register(data: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    display_name?: string;
  }): Promise<AuthResponse> {
    const res = await api.post<AuthResponse>('/auth/register/', data);
    localStorage.setItem('resumesense_access_token', res.data.tokens.access);
    localStorage.setItem('resumesense_refresh_token', res.data.tokens.refresh);
    return res.data;
  },

  async login(credentials: { username: string; password: string }): Promise<AuthResponse> {
    const res = await api.post<AuthResponse>('/auth/login/', credentials);
    localStorage.setItem('resumesense_access_token', res.data.tokens.access);
    localStorage.setItem('resumesense_refresh_token', res.data.tokens.refresh);
    return res.data;
  },

  async getMe(): Promise<User> {
    const res = await api.get<User>('/auth/me/');
    return res.data;
  },

  async getProfile(): Promise<User> {
    const res = await api.get<User>('/auth/me/');
    return res.data;
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const res = await api.patch<User>('/auth/profile/', data);
    return res.data;
  },

  async changePassword(data: { old_password: string; new_password: string }): Promise<void> {
    await api.post('/auth/change-password/', data);
  },

  logout(): void {
    localStorage.removeItem('resumesense_access_token');
    localStorage.removeItem('resumesense_refresh_token');
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('resumesense_access_token');
  }
};
