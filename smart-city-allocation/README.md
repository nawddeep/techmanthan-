# 🏙️ Smart City Resource Allocation Command Center

An AI-powered, real-time command center dashboard designed to simulate and manage Smart City resources in Udaipur. The system continuously ingests real-time simulated data based on real-world urban patterns, with live weather API integration, runs highly trained machine learning predictive models, and surfaces critical metrics to city operators through a stunning Next.js interface.

### 🌟 Key Features
- **Real-Time Simulation Engine**: A continuous background daemon simulating city-wide telemetry data (traffic, waste levels, incidents).
- **Traffic Congestion AI**: Predicts traffic congestion and recommends dynamic rerouting based on historical machine learning data.
- **Waste Overflow AI**: Monitors waste bin fill percentages and triggers immediate collection vehicles to avoid hazardous overflow.
- **Rapid Emergency Response Layout**: Tracks active emergencies across sectors and surfaces actionable incident control insights.
- **Interactive Tracking Map**: Integrated Leaflet capabilities marking precise problem areas, dynamically rerendering with the latest data.

---

## 🏗️ Architecture

> **Data Transparency**: Traffic and waste signals are simulated using real-world behavioral patterns, while weather data is fetched from a live API. We simulate urban data in real time using realistic behavioral patterns, and integrate live APIs where available to demonstrate hybrid system capability.

The project has evolved into a robust decoupled system:
* **Frontend**: Modern `Next.js 14` App Router using `TailwindCSS` for gorgeous, high-fidelity responsive design. Employs `Lucide React` and `Recharts` for intuitive dataviz.
* **Backend**: High-performance `FastAPI` (Python) acting as the main simulation core. Runs an internal asynchronous event loop simulating real city events, handling Data Engineering, and executing Scikit-Learn `.pkl` models.

---

## 🚀 Quick Start Guide

### 1. Launching the Backend (FastAPI Core)
Ensure you have Python 3.9+ installed. From the `smart-city-allocation` directory:
```bash
# Activate your virtual environment
source venv/bin/activate

# Start the uvicorn server with Hot-Reload enabled
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend initializes the Machine Learning models into memory and starts the background simulation daemon immediately on startup.

### 2. Launching the Frontend (Next.js Dashboard)
Open a new terminal session. From the `smart-city-allocation/frontend` directory:
```bash
# Install dependencies (only required once)
npm install

# Start the development server
npm run dev
```
Navigate your browser to [http://localhost:3000](http://localhost:3000). The dashboard proxy is deeply integrated to bypass frontend CORS requirements securely by communicating directly with the `127.0.0.1:8000` AI endpoints!

---

## 📂 Repository Structure

```
smart-city-allocation/
├── api/                  # Python FastAPI application
│   ├── routes/           # Endpoints for Traffic, Waste, Emergency, Map
│   ├── services/         # Scikit-Learn ML implementations & Sim Engine
│   └── main.py           # Application Entry Point
├── data/                 # Raw datasets for historical contexts
├── frontend/             # Next.js 14 Dashboard 
│   ├── src/app/          # Core views
│   └── src/components/   # Modular React functional components
├── traffic_model.pkl     # Pre-trained ML weights for traffic flow
└── waste_model.pkl       # Pre-trained ML weights for waste prediction
```

> **Note**: Legacy Streamlit visualization `.py` files and localized data generation pipelines were removed from the central GitHub repository to ensure a perfectly clean production environment. All AI meta-configurations reside locally and are completely untracked to keep git diffs seamless.
