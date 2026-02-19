import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { flightAPI, planetAPI } from '../services/api';

export default function Flights() {
  const [flights, setFlights] = useState([]);
  const [planets, setPlanets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    origin: '',
    destination: '',
    priceMin: 0,
    priceMax: 50000,
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [flightsData, planetsData] = await Promise.all([
        flightAPI.getAll(),
        planetAPI.getAll(),
      ]);
      setFlights(flightsData.results || flightsData);
      setPlanets(planetsData.results || planetsData);
    } catch (err) {
      setError('Failed to load flights. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredFlights = flights.filter((flight) => {
    const originMatch = !filters.origin || flight.origin_planet?.id === parseInt(filters.origin);
    const destMatch =
      !filters.destination ||
      flight.destination_planet?.id === parseInt(filters.destination);
    const priceMatch =
      flight.price_credits >= filters.priceMin &&
      flight.price_credits <= filters.priceMax;

    return originMatch && destMatch && priceMatch;
  });

  const formatDateTime = (dateTime) => {
    if (!dateTime) return 'N/A';
    return new Date(dateTime).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="section-padding bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
      <div className="container-max">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Available Flights
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl">
            Browse and book your next space journey. Find the perfect flight to your destination.
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Origin */}
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Departure From
              </label>
              <select
                value={filters.origin}
                onChange={(e) => setFilters({ ...filters, origin: e.target.value })}
                className="input-field"
              >
                <option value="">All Origins</option>
                {planets.map((planet) => (
                  <option key={planet.id} value={planet.id}>
                    {planet.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Destination */}
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Destination
              </label>
              <select
                value={filters.destination}
                onChange={(e) =>
                  setFilters({ ...filters, destination: e.target.value })
                }
                className="input-field"
              >
                <option value="">All Destinations</option>
                {planets.map((planet) => (
                  <option key={planet.id} value={planet.id}>
                    {planet.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Price Min */}
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Min Price (credits)
              </label>
              <input
                type="number"
                value={filters.priceMin}
                onChange={(e) =>
                  setFilters({ ...filters, priceMin: parseInt(e.target.value) || 0 })
                }
                className="input-field"
              />
            </div>

            {/* Price Max */}
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Max Price (credits)
              </label>
              <input
                type="number"
                value={filters.priceMax}
                onChange={(e) =>
                  setFilters({ ...filters, priceMax: parseInt(e.target.value) || 50000 })
                }
                className="input-field"
              />
            </div>
          </div>
        </div>

        {/* Results */}
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
        ) : filteredFlights.length === 0 ? (
          <div className="p-12 bg-white rounded-xl text-center">
            <p className="text-gray-600 text-lg mb-4">No flights found matching your criteria.</p>
            <button
              onClick={() =>
                setFilters({
                  origin: '',
                  destination: '',
                  priceMin: 0,
                  priceMax: 50000,
                })
              }
              className="btn-secondary"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredFlights.map((flight) => (
              <Link
                key={flight.id}
                to={`/flights/${flight.id}/book`}
                className="card card-hover p-6"
              >
                <div className="grid grid-cols-1 md:grid-cols-5 gap-6 items-center">
                  {/* Route */}
                  <div>
                    <p className="text-gray-600 text-sm mb-1">Route</p>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-gray-900">
                        {flight.origin_planet?.name || 'Unknown'}
                      </span>
                      <span className="text-blue-600">→</span>
                      <span className="font-semibold text-gray-900">
                        {flight.destination_planet?.name || 'Unknown'}
                      </span>
                    </div>
                  </div>

                  {/* Departure */}
                  <div>
                    <p className="text-gray-600 text-sm mb-1">Departure</p>
                    <p className="font-semibold text-gray-900">
                      {formatDateTime(flight.departure_datetime)}
                    </p>
                  </div>

                  {/* Duration */}
                  <div>
                    <p className="text-gray-600 text-sm mb-1">Duration</p>
                    <p className="font-semibold text-gray-900">
                      {flight.destination_planet?.travel_time_days || 'N/A'} days
                    </p>
                  </div>

                  {/* Availability */}
                  <div>
                    <p className="text-gray-600 text-sm mb-1">Seats Available</p>
                    <p className="font-semibold text-gray-900">
                      {flight.seats_available} / {flight.seats_total}
                    </p>
                  </div>

                  {/* Price */}
                  <div className="text-right">
                    <p className="text-gray-600 text-sm mb-1">Price per Seat</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {flight.price_credits?.toLocaleString()} cr
                    </p>
                    <p className="text-xs text-gray-600 mt-2">Book →</p>
                  </div>
                </div>

                {/* Status Badge */}
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <span
                    className={`badge-primary text-xs font-semibold ${
                      flight.status === 'scheduled'
                        ? 'badge-secondary'
                        : flight.status === 'in_progress'
                          ? 'badge-accent'
                          : 'badge-danger'
                    }`}
                  >
                    {flight.status?.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Results Count */}
        {!loading && !error && filteredFlights.length > 0 && (
          <div className="mt-8 text-center text-gray-600">
            <p>
              Showing {filteredFlights.length} of {flights.length} flights
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
