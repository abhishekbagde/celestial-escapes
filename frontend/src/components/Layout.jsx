import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store';

export default function Layout({ children }) {
  const navigate = useNavigate();
  const { isAuthenticated, logout, user } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-space-900 via-space-800 to-space-900">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-gradient-to-r from-space-900/95 to-space-800/95 backdrop-blur-sm border-b border-cosmic-cyan/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <span className="text-2xl">✨</span>
              <span className="text-xl font-bold bg-gradient-to-r from-cosmic-cyan to-cosmic-glow bg-clip-text text-transparent">
                Celestial Escapes
              </span>
            </Link>

            {/* Nav Links */}
            <div className="hidden md:flex items-center space-x-8">
              <Link
                to="/planets"
                className="text-cosmic-purple hover:text-cosmic-cyan transition"
              >
                Planets
              </Link>
              <Link
                to="/flights"
                className="text-cosmic-purple hover:text-cosmic-cyan transition"
              >
                Flights
              </Link>
              {isAuthenticated && (
                <Link
                  to="/dashboard"
                  className="text-cosmic-purple hover:text-cosmic-cyan transition"
                >
                  Dashboard
                </Link>
              )}
            </div>

            {/* Auth Links */}
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <span className="text-cosmic-purple">
                    Welcome, {user?.username || 'Traveler'}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="btn-cosmic px-4 py-2 text-sm"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="text-cosmic-cyan hover:text-cosmic-glow transition"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="btn-cosmic px-4 py-2 text-sm"
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-space-900/50 border-t border-cosmic-cyan/20 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-cosmic-purple/60 text-sm">
            <p>&copy; 2026 Celestial Escapes. Explore the universe responsibly.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
