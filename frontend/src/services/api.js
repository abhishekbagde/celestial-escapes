import axios from 'axios';

const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const planetAPI = {
  getAll: () => api.get('/planets/'),
  get: (slug) => api.get(`/planets/${slug}/`),
};

export const flightAPI = {
  getAll: (params) => api.get('/flights/', { params }),
  get: (id) => api.get(`/flights/${id}/`),
  create: (data) => api.post('/flights/', data),
};

export const podAPI = {
  getAll: (params) => api.get('/pods/', { params }),
  get: (id) => api.get(`/pods/${id}/`),
};

export const bookingAPI = {
  getAll: () => api.get('/bookings/'),
  get: (id) => api.get(`/bookings/${id}/`),
  create: (data) => api.post('/bookings/', data),
  confirm: (id) => api.post(`/bookings/${id}/confirm/`),
  cancel: (id) => api.post(`/bookings/${id}/cancel/`),
};

export const authAPI = {
  register: (data) => api.post('/users/', data),
  login: (username, password) => 
    api.post('/auth-token/', { username, password }),
  getMe: () => api.get('/users/me/'),
};

export const profileAPI = {
  getMe: () => api.get('/profiles/me/'),
  update: (id, data) => api.put(`/profiles/${id}/`, data),
};

export default api;
