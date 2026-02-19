import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { usePlanetStore } from '../store';
import { planetAPI } from '../services/api';

export default function Home() {
  const { planets, setPlanets, setLoading } = usePlanetStore();

  useEffect(() => {
    const fetchPlanets = async () => {
      setLoading(true);
      try {
        const { data } = await planetAPI.getAll();
        setPlanets(data.results || data);
      } catch (err) {
        console.error('Failed to fetch planets:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPlanets();
  }, []);

  return (
    <div>
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-b from-space-900 to-space-800 overflow-hidden">
        {/* Animated starfield */}
        <div className="absolute inset-0 opacity-20">
          {Array.from({ length: 100 }).map((_, i) => (
            <div
              key={i}
              className="star"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                width: `${Math.random() * 3}px`,
                height: `${Math.random() * 3}px`,
                animationDelay: `${Math.random() * 3}s`,
              }}
            />
          ))}
        </div>

        <div className="relative z-10 text-center max-w-4xl mx-auto px-4">
          <h1 className="text-6xl md:text-8xl font-black mb-6 bg-gradient-to-r from-cosmic-cyan via-cosmic-glow to-cosmic-cyan bg-clip-text text-transparent">
            ✨ CELESTIAL ESCAPES ✨
          </h1>

          <p className="text-xl md:text-2xl text-cosmic-purple mb-12 max-w-2xl mx-auto">
            Journey Beyond the Stars — Explore the Universe Like Never Before
          </p>

          <div className="flex flex-col md:flex-row gap-6 justify-center">
            <Link
              to="/planets"
              className="btn-cosmic flex items-center justify-center"
            >
              🌍 Explore Planets
            </Link>
            <Link
              to="/flights"
              className="btn-cosmic flex items-center justify-center"
            >
              🚀 Book Flight
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-b from-space-800 to-space-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-16 bg-gradient-to-r from-cosmic-cyan to-cosmic-glow bg-clip-text text-transparent">
            Why Choose Celestial Escapes?
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: '🛡️',
                title: 'Safe Journeys',
                description: 'State-of-the-art spacecraft with perfect safety records.',
              },
              {
                icon: '⭐',
                title: 'Luxury Experience',
                description: 'Experience unparalleled comfort and amenities.',
              },
              {
                icon: '📞',
                title: '24/7 Support',
                description: 'Mission control team ready to assist you anytime.',
              },
            ].map((feature, i) => (
              <div key={i} className="card group hover:translate-y-[-10px] transition-all">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-cosmic-cyan mb-3">
                  {feature.title}
                </h3>
                <p className="text-cosmic-purple">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Destinations Preview */}
      {planets.length > 0 && (
        <section className="py-20 bg-space-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-4xl font-bold text-center mb-16 bg-gradient-to-r from-cosmic-cyan to-cosmic-glow bg-clip-text text-transparent">
              Featured Destinations
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {planets.slice(0, 4).map((planet) => (
                <Link
                  key={planet.id}
                  to={`/planets/${planet.slug}`}
                  className="card group"
                >
                  <div className="text-5xl mb-4 text-center">{planet.emoji}</div>
                  <h3 className="text-xl font-bold text-cosmic-cyan mb-2">
                    {planet.name}
                  </h3>
                  <p className="text-sm text-cosmic-purple mb-4 line-clamp-2">
                    {planet.description}
                  </p>
                  <div className="text-xs text-cosmic-purple/60">
                    {planet.distance_from_earth_km}M km away
                  </div>
                </Link>
              ))}
            </div>

            <div className="text-center mt-12">
              <Link to="/planets" className="btn-cosmic">
                View All Destinations
              </Link>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
