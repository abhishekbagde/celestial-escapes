import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: !!localStorage.getItem('authToken'),
  token: localStorage.getItem('authToken') || null,
  loading: false,
  error: null,

  setUser: (user) => set({ user }),
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
