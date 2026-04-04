# Smart City Command Center - Frontend

A world-class, real-time dashboard for smart city resource allocation with zero hallucination and live data visualization.

## 🚀 Features

### Core Capabilities
- **Real-time Data Visualization** - Live updates via WebSocket with polling fallback
- **Interactive City Map** - Full-screen capable map with emergency heat layers
- **Zero Hallucination** - Clear data source indicators (REAL DATA vs SIMULATED)
- **ML Predictions** - Traffic, waste, and emergency predictions with confidence scores
- **SHAP Explainability** - Understand why the AI made specific decisions
- **JWT Authentication** - Secure access with role-based permissions
- **Responsive Design** - Works on desktop, tablet, and mobile

### Map Features
- ✅ **Larger Map** - 600px height (expandable to fullscreen)
- ✅ **Fullscreen Mode** - Immersive map experience
- ✅ **Emergency Heat Layer** - Toggle between normal and emergency views
- ✅ **Live Data Indicators** - Always know if you're viewing real or simulated data
- ✅ **Enhanced Markers** - Larger, more visible zone markers with detailed popups
- ✅ **Auto-fit Bounds** - Automatically centers on all city zones
- ✅ **Zoom Controls** - Easy navigation with built-in zoom buttons

## 🛠️ Tech Stack

- **Framework**: Next.js 16 (React 19)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Maps**: Leaflet + React Leaflet
- **Charts**: Recharts
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Animations**: Framer Motion

## 📦 Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local with your backend URL
# NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
# NEXT_PUBLIC_WS_URL=ws://127.0.0.1:8000/ws/city-updates
```

## 🚀 Development

```bash
# Start development server
npm run dev

# Open browser
# http://localhost:3000
```

## 🏗️ Build for Production

```bash
# Build optimized production bundle
npm run build

# Start production server
npm start
```

## 📊 Data Source Indicators

The dashboard clearly shows the data source at all times:

- **🟢 REAL DATA** - Green badge = Actual data from sensors/APIs
- **🟡 STAT SIM** - Yellow badge = Statistical simulation
- **🟡 LIVE** - Yellow badge = Live simulation
- **🟡 CACHED** - Yellow badge = Cached data

This ensures **ZERO HALLUCINATION** - you always know what you're looking at.

## 🗺️ Map Controls

1. **Normal View** - Shows traffic and waste ML predictions
2. **Emergency Heat Layer** - Shows emergency risk scores
3. **Fullscreen Mode** - Click maximize icon for immersive view
4. **Zoom Controls** - Top-right corner of map
5. **Click Markers** - View detailed zone information

## 🎨 UI Components

- `MapComponent` - Main map with fullscreen and heat layer controls
- `LiveLeafletMap` - Leaflet integration with auto-fit bounds
- `KPICard` - Key performance indicators with sparklines
- `AlertPanel` - Real-time alerts and warnings
- `DecisionPanel` - AI-recommended actions
- `Charts` - Historical trend visualization
- `HealthScoreCard` - Overall city health score
- `ROICard` - Return on investment calculations

## 🔐 Authentication

The frontend uses JWT tokens stored in HttpOnly cookies:

1. Login at `/login`
2. Token automatically refreshed on expiry
3. Automatic redirect to login on 401 errors
4. WebSocket authentication via token query param

## 🌐 API Integration

All API calls go through `/api/bff` (Backend-for-Frontend):

- Automatic token refresh on 401
- Retry logic for failed requests
- CORS handling
- Error boundaries for graceful failures

## 📱 Responsive Design

- **Mobile**: Single column layout
- **Tablet**: 2-column grid
- **Desktop**: 3-5 column grid
- **Large Desktop**: Full 5-column layout

## 🎯 Performance Optimizations

- Dynamic imports for map (reduces initial bundle)
- Memoized map markers (prevents unnecessary re-renders)
- Debounced WebSocket updates
- Lazy loading for charts
- Optimized images and assets

## 🐛 Error Handling

- Error boundaries around each component
- Graceful fallbacks for failed API calls
- Stale data warnings (>30s without update)
- Connection status indicators
- Retry mechanisms

## 📈 Future Enhancements

- [ ] Dark/Light theme toggle
- [ ] Custom map layers (satellite, terrain)
- [ ] Export data to CSV/PDF
- [ ] Advanced filtering and search
- [ ] Historical playback mode
- [ ] Multi-city support
- [ ] Mobile app (React Native)

## 🤝 Contributing

This is a hackathon project. Feel free to fork and improve!

## 📄 License

MIT License - See LICENSE file for details
