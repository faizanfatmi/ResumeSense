import axios from 'axios';

// Base URL for the backend API. On Render (separate frontend/backend hosts)
// set VITE_API_URL, e.g. https://resumesense-backend.onrender.com/api.
// Locally and under docker-compose it is unset, so requests use the relative
// "/api" path, which the Vite dev server / nginx proxy to the backend.
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach access token to outgoing requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('resumesense_access_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('resumesense_refresh_token');
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE_URL}/auth/refresh/`, { refresh: refreshToken });
          const newAccess = res.data.access;
          localStorage.setItem('resumesense_access_token', newAccess);
          originalRequest.headers.Authorization = `Bearer ${newAccess}`;
          return api(originalRequest);
        } catch (refreshErr) {
          localStorage.removeItem('resumesense_access_token');
          localStorage.removeItem('resumesense_refresh_token');
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
