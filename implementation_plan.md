# Celestial Escapes — Full Rebuild Plan

A space travel booking web app with immersive 3D planet rendering using real NASA assets, authentication, flight/pod booking, and account management.

---

## ⚡ Tech Stack Decision

### Why NOT pure Django templates?
Django is great for backend logic, but it has a hard limitation for 3D rendering — you need a rich JavaScript runtime with WebGL to render glTF/USDZ models interactively. Django's Jinja/template system alone can't handle that.

### ✅ Recommended Stack: Django REST Framework + React (Vite)

| Layer | Technology | Why |
|---|---|---|
| **Backend API** | Django + Django REST Framework | Auth, models, bookings — all in Python. Keeps existing DB setup. |
| **Frontend** | React (via Vite) | Modern component model, fast hot-reload, great for 3D integration |
| **3D Rendering** | `@google/model-viewer` + Three.js | model-viewer for glTF planet display; Three.js for custom solar system scene |
| **3D Assets** | NASA glTF models (NASA Science + Sketchfab) | Free, official NASA 3D assets in web-ready glTF format |
| **Database** | PostgreSQL | ✅ Already configured. Best for relational data: users, bookings, planets |
| **Auth** | Django's built-in auth + DRF Token Auth | Simple, secure, well-tested |
| **Styling** | Tailwind CSS (via Vite) | Rapid UI dev, dark-mode ready for space aesthetic |
| **State** | Zustand (lightweight React state) | Simple global state for auth/cart |

> [!IMPORTANT]
> This is a **hybrid architecture**: Django serves the REST API on port 8000, React (Vite) runs on port 5173 in dev. In production, Django's `whitenoise` serves the built React bundle via `collectstatic`.

---

## 🗄️ Database Design (PostgreSQL)

PostgreSQL is the **right choice** because:
- Relational: Users → Bookings → Flights/Pods are perfectly modeled with FK relations
- JSON fields for flexible planet metadata
- Already configured in your [.env](file:///Users/abhishekbagde/Documents/hack/celestial-escapes/.env)
- Production-battle-tested

### Key Models

```
User (Django built-in)
  └── Profile (avatar, bio, passport_id, planet_pref)

Planet
  ├── name, slug, description
  ├── gltf_model_url  ← NASA/Sketchfab URL or local path
  ├── distance_from_earth_ly (float)
  └── travel_time_days (int)

Flight
  ├── origin_planet FK Planet
  ├── destination_planet FK Planet
  ├── departure_datetime
  ├── seats_total / seats_available
  └── price_credits (decimal)

Pod  (sleeping pod / luxury suite)
  ├── flight FK Flight
  ├── pod_type (Standard / Luxury / Cryo)
  └── price_credits

Booking
  ├── user FK User
  ├── flight FK Flight
  ├── pod FK Pod (nullable)
  ├── status (pending / confirmed / cancelled)
  └── booked_at
```

---

## 🌌 3D Planet Rendering

### Source for NASA models
- **[NASA Science 3D Resources](https://science.nasa.gov/solar-system/resources/)** — official glTF downloads for Mars, Jupiter, Moon, etc.
- **[NASA GitHub](https://github.com/nasa/NASA-3D-Resources)** — growing collection
- **Sketchfab NASA account** — 60+ NASA models in glTF/GLB format (free download)

### Rendering approach
Use **`@google/model-viewer`** as HTML web component — zero-config, handles WebGL, AR, loading states:
```html
<model-viewer
  src="/static/models/mars.glb"
  auto-rotate
  camera-controls
  shadow-intensity="1"
  environment-image="neutral"
/>
```
For the hero solar system scene, use **Three.js** with orbit controls for an interactive map showing all destinations.

---

## 📱 Pages & User Flow

```
/                → Hero landing (Three.js solar system)
/login           → Login page (email + password)
/register        → Register page
/dashboard       → After login: Book Flight / Book Pod / Settings
/planets         → Planet catalog with model-viewer 3D previews
/planets/:slug   → Planet detail (full 3D + info + available flights)
/book/flight     → Flight search & booking
/book/pod        → Pod selection after flight booking
/account         → Profile settings (avatar, name, preferences)
/bookings        → My bookings history
```

---

## 🏗️ Build Phases

### Phase 1 — Backend Foundation
- [ ] Set up DRF with token auth
- [ ] Build Planet, Flight, Pod, Booking, Profile models + migrations
- [ ] Seed database with NASA planets data
- [ ] Expose REST API endpoints (`/api/v1/`)

### Phase 2 — React Frontend Scaffold
- [ ] Create Vite + React app inside `frontend/` directory
- [ ] Configure Tailwind CSS with space dark-mode theme
- [ ] Set up React Router for all routes
- [ ] Configure Vite proxy to Django API

### Phase 3 — Auth Pages
- [ ] Login page (JWT/token)
- [ ] Register page
- [ ] Protected route HOC

### Phase 4 — 3D Planet Experience
- [ ] Download NASA glTF models for 8+ planets
- [ ] Integrate `model-viewer` for planet cards
- [ ] Build Three.js solar system hero scene

### Phase 5 — Booking Flow
- [ ] Flight search & listing
- [ ] Pod selection
- [ ] Booking confirmation

### Phase 6 — Account Settings
- [ ] Profile update (name, avatar upload, preferences)
- [ ] Booking history

---

## ✅ Verification Plan

### Automated
- Django test suite: `python manage.py test` (model tests, API endpoint tests)
- React component tests: `npm test` (via Vitest)

### Manual browser verification (using browser tool)
1. Open `http://localhost:5173` → confirm hero 3D solar system loads
2. Register + login → confirm redirect to dashboard
3. Navigate to a planet → confirm glTF model spins in model-viewer
4. Book a flight → confirm booking appears in `/bookings`
5. Update profile → confirm changes persist after refresh

> [!NOTE]
> We'll build phase by phase. You can approve this plan and I'll start with Phase 1 (backend) + Phase 2 (React scaffold) together.
