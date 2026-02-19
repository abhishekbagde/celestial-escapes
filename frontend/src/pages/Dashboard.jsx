import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store';
import { bookingAPI, profileAPI } from '../services/api';

export default function Dashboard() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const [bookings, setBookings] = useState([]);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    fetchData();
  }, [isAuthenticated, navigate]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [bookingsData, profileData] = await Promise.all([
        bookingAPI.getAll(),
        profileAPI.getMe(),
      ]);
      setBookings(bookingsData.results || bookingsData);
      setProfile(profileData);
    } catch (err) {
      setError('Failed to load dashboard data.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const formatDateTime = (dateTime) => {
    if (!dateTime) return 'N/A';
    return new Date(dateTime).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="section-padding bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
      <div className="container-max">
        {/* Header */}
        <div className="flex justify-between items-start mb-12">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-2">
              Welcome, {user?.first_name || user?.username || 'Traveler'}!
            </h1>
            <p className="text-lg text-gray-600">
              Manage your bookings and account settings
            </p>
          </div>
          <button onClick={handleLogout} className="btn-secondary">
            Logout
          </button>
        </div>

        {/* Profile Card */}
        {profile && (
          <div className="card p-8 mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Profile Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-gray-600 text-sm mb-1">Full Name</p>
                <p className="text-lg font-semibold text-gray-900">
                  {user?.first_name} {user?.last_name}
                </p>
              </div>
              <div>
                <p className="text-gray-600 text-sm mb-1">Email</p>
                <p className="text-lg font-semibold text-gray-900">{user?.email}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm mb-1">Username</p>
                <p className="text-lg font-semibold text-gray-900">{user?.username}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm mb-1">Member Since</p>
                <p className="text-lg font-semibold text-gray-900">
                  {new Date(user?.date_joined || Date.now()).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Bookings Section */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Bookings</h2>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="spinner"></div>
            </div>
          ) : error ? (
            <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-center">
              <p className="text-red-700">{error}</p>
              <button onClick={fetchData} className="btn-primary mt-4">
                Try Again
              </button>
            </div>
          ) : bookings.length === 0 ? (
            <div className="card p-12 text-center">
              <p className="text-gray-600 text-lg mb-4">
                You haven't made any bookings yet.
              </p>
              <button
                onClick={() => navigate('/flights')}
                className="btn-primary"
              >
                Browse Flights
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {bookings.map((booking) => (
                <div key={booking.id} className="card p-6">
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-center">
                    {/* Route */}
                    <div>
                      <p className="text-gray-600 text-sm mb-1">Route</p>
                      <p className="font-semibold text-gray-900">
                        {booking.flight?.origin_planet?.name} →{' '}
                        {booking.flight?.destination_planet?.name}
                      </p>
                    </div>

                    {/* Departure */}
                    <div>
                      <p className="text-gray-600 text-sm mb-1">Departure</p>
                      <p className="font-semibold text-gray-900">
                        {formatDateTime(booking.flight?.departure_datetime)}
                      </p>
                    </div>

                    {/* Pod */}
                    <div>
                      <p className="text-gray-600 text-sm mb-1">Pod</p>
                      <p className="font-semibold text-gray-900">
                        {booking.pod?.pod_number} ({booking.pod?.pod_type})
                      </p>
                    </div>

                    {/* Price */}
                    <div>
                      <p className="text-gray-600 text-sm mb-1">Total Price</p>
                      <p className="text-lg font-bold text-blue-600">
                        {booking.total_price?.toLocaleString()} cr
                      </p>
                    </div>

                    {/* Status */}
                    <div className="text-right">
                      <span
                        className={`badge-primary text-xs font-semibold ${
                          booking.status === 'confirmed'
                            ? 'badge-success'
                            : booking.status === 'pending'
                              ? 'badge-accent'
                              : 'badge-danger'
                        }`}
                      >
                        {booking.status?.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="mt-4 pt-4 border-t border-gray-200 flex gap-2">
                    <button className="btn-secondary text-sm">View Details</button>
                    {booking.status === 'pending' && (
                      <button className="btn-ghost text-sm">Cancel Booking</button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
