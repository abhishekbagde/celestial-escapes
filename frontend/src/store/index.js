import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  isAuthenticated: !!localStorage.getItem('authToken'),
  token: localStorage.getItem('authToken') || null,
  loading: false,
  error: null,

  setAuth: (user, token) => {
    localStorage.setItem('authToken', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ user, token, isAuthenticated: true });
  },
  setUser: (user) => {
    localStorage.setItem('user', JSON.stringify(user));
    set({ user });
  },
  setToken: (token) => {
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
    set({ token, isAuthenticated: !!token });
  },
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    set({ user: null, token: null, isAuthenticated: false });
  },
}));

export const useBookingStore = create((set) => ({
  cart: {
    flight: null,
    pod: null,
    passengers: 1,
  },
  setFlight: (flight) => set((state) => ({
    cart: { ...state.cart, flight },
  })),
  setPod: (pod) => set((state) => ({
    cart: { ...state.cart, pod },
  })),
  setPassengers: (passengers) => set((state) => ({
    cart: { ...state.cart, passengers },
  })),
  clearCart: () => set({
    cart: { flight: null, pod: null, passengers: 1 },
  }),
}));

export const usePlanetStore = create((set) => ({
  planets: [],
  selectedPlanet: null,
  loading: false,

  setPlanets: (planets) => set({ planets }),
  setSelectedPlanet: (planet) => set({ selectedPlanet: planet }),
  setLoading: (loading) => set({ loading }),
}));
