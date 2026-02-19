import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { planetAPI } from '../services/api';

export default function Planets() {
  const [planets, setPlanets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    distanceMin: 0,
    distanceMax: 10000,
    travelTimeMin: 0,
    travelTimeMax: 365,
  });

  useEffect(() => {
    fetchPlanets();
  }, []);

  const fetchPlanets = async () => {
    try {
      setLoading(true);
      const data = await planetAPI.getAll();
      setPlanets(data.results || data);
    } catch (err) {
      setError('Failed to load planets. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredPlanets = planets.filter((planet) => {
    const matchesSearch =
      planet.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      planet.description.toLowerCase().includes(searchTerm.toLowerCase());

    const distance = planet.distance_from_earth_km || 0;
    const travelTime = planet.travel_time_days || 0;

    const matchesFilters =
      distance >= filters.distanceMin &&
      distance <= filters.distanceMax &&
      travelTime >= filters.travelTimeMin &&
      travelTime <= filters.travelTimeMax;

    return matchesSearch && matchesFilters;
  });

  return (
    <div className="section-padding bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
      <div className="container-max">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Explore Our Destinations
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl">
            Discover amazing planets and moons waiting for your exploration. Choose your next adventure.
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-12">
          {/* Search */}
          <div className="mb-6">
            <input
              type="text"
              placeholder="Search planets by name or description..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field w-full"
            />
          </div>

          {/* Filters */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Min Distance (km)
              </label>
              <input
                type="number"
                value={filters.distanceMin}
                onChange={(e) =>
                  setFilters({ ...filters, distanceMin: parseInt(e.target.value) || 0 })
                }
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Max Distance (km)
              </label>
              <input
                type="number"
                value={filters.distanceMax}
                onChange={(e) =>
                  setFilters({ ...filters, distanceMax: parseInt(e.target.value) || 10000 })
                }
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Min Travel Time (days)
              </label>
              <input
                type="number"
                value={filters.travelTimeMin}
                onChange={(e) =>
                  setFilters({ ...filters, travelTimeMin: parseInt(e.target.value) || 0 })
                }
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">
                Max Travel Time (days)
              </label>
              <input
                type="number"
                value={filters.travelTimeMax}
                onChange={(e) =>
                  setFilters({ ...filters, travelTimeMax: parseInt(e.target.value) || 365 })
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
            <button onClick={fetchPlanets} className="btn-primary mt-4">
              Try Again
            </button>
          </div>
        ) : filteredPlanets.length === 0 ? (
          <div className="p-12 bg-white rounded-xl text-center">
            <p className="text-gray-600 text-lg mb-4">No planets found matching your criteria.</p>
            <button
              onClick={() => {
                setSearchTerm('');
                setFilters({
                  distanceMin: 0,
                  distanceMax: 10000,
                  travelTimeMin: 0,
                  travelTimeMax: 365,
                });
              }}
              className="btn-secondary"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="grid-cols-responsive">
            {filteredPlanets.map((planet) => (
              <Link
                key={planet.id}
                to={`/planets/${planet.slug}`}
                className="card card-hover group"
              >
                {/* Planet Image Placeholder */}
                <div className="h-48 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg mb-4 flex items-center justify-center overflow-hidden">
                  <div className="text-6xl group-hover:scale-110 transition-transform duration-300">
                    {planet.emoji || '🌍'}
                  </div>
                </div>

                {/* Planet Info */}
                <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                  {planet.name}
                </h3>

                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {planet.description}
                </p>

                {/* Stats */}
                <div className="space-y-2 text-sm text-gray-700 mb-4 border-t border-gray-200 pt-4">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Distance from Earth:</span>
                    <span className="font-semibold">{planet.distance_from_earth_km?.toLocaleString()} km</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Travel Time:</span>
                    <span className="font-semibold">{planet.travel_time_days} days</span>
                  </div>
                </div>

                {/* CTA */}
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <span className="text-blue-600 font-semibold text-sm">
                    View Details →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Results Count */}
        {!loading && !error && filteredPlanets.length > 0 && (
          <div className="mt-8 text-center text-gray-600">
            <p>
              Showing {filteredPlanets.length} of {planets.length} planets
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
