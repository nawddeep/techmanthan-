# Smart City Production Upgrade - Requirements

## Feature Overview

Upgrade the Smart City hackathon project from prototype to production-ready system with proper ML pipeline, authentication, data persistence, real-time communication, and deployment infrastructure.

## Requirements

### Requirement 1: ML Model Training Pipeline

**User Story:** As a data scientist, I want a reproducible model training pipeline, so that I can retrain models with new data and validate their performance.

#### Acceptance Criteria

1. WHEN the training notebook is executed THEN the system SHALL load all three CSV datasets (traffic_clean.csv, waste_clean.csv, emergency_clean.csv)
2. WHEN performing EDA THEN the system SHALL display data shape, null counts, class balance, and correlation heatmaps
3. WHEN preprocessing data THEN the system SHALL apply label encoding, StandardScaler, and stratified train/test split (80/20)
4. WHEN training models THEN the system SHALL train three model types (RandomForest, GradientBoosting, XGBoost) for both traffic and waste
5. WHEN evaluating models THEN the system SHALL perform 5-fold stratified cross-validation and display classification reports, confusion matrices, and ROC-AUC scores
6. WHEN selecting best models THEN the system SHALL save the best performing model for each task as traffic_model.pkl and waste_model.pkl
7. WHEN training emergency model THEN the system SHALL train and save emergency_model.pkl from emergency_clean.csv
8. WHEN generating visualizations THEN the system SHALL save feature importance plots as PNG files in notebooks/plots/

### Requirement 2: Real Data Simulation

**User Story:** As a system operator, I want the simulation to use real data patterns, so that predictions reflect actual urban behavior.

#### Acceptance Criteria

1. WHEN the simulation service starts THEN the system SHALL load all three CSV files from the /data/ directory
2. WHEN generating city state THEN the system SHALL sample from real CSV data using actual statistical distributions
3. WHEN updating traffic levels THEN the system SHALL weight sampling by time of day using the hour column from traffic data
4. WHEN updating waste levels THEN the system SHALL use actual bin_fill_pct progression rates from the data
5. WHEN CSV files are not found THEN the system SHALL gracefully fall back to statistical simulation
6. WHEN exposing state THEN the system SHALL include a data_source field indicating "real_data" or "statistical_sim"
7. WHEN maintaining state THEN the system SHALL keep a rolling window of last 50 real samples per location

### Requirement 3: Emergency ML Service

**User Story:** As an emergency coordinator, I want ML-based emergency risk predictions, so that I can proactively allocate response resources.

#### Acceptance Criteria

1. WHEN the emergency service starts THEN the system SHALL load emergency_model.pkl
2. WHEN predicting emergency risk THEN the system SHALL accept zone, hour, day_of_week, weather, and road_condition parameters
3. WHEN generating predictions THEN the system SHALL return risk_score (float), high_risk (bool), and confidence (float)
4. WHEN the model is not loaded THEN the system SHALL fall back to rule-based scoring
5. WHEN explaining predictions THEN the system SHALL provide SHAP explainability matching the existing pattern
6. WHEN generating decisions THEN the system SHALL call emergency ML service for all 10 locations and include worst-case zone

### Requirement 4: Secure Authentication

**User Story:** As a system administrator, I want proper authentication with bcrypt and JWT, so that only authorized users can access the system.

#### Acceptance Criteria

1. WHEN hashing passwords THEN the system SHALL use passlib with bcrypt (not string concatenation)
2. WHEN storing secrets THEN the system SHALL read SECRET_KEY from environment variables only
3. WHEN creating tokens THEN the system SHALL generate JWT tokens with proper expiry
4. WHEN validating tokens THEN the system SHALL verify JWT signature and expiry
5. WHEN implementing RBAC THEN the system SHALL enforce admin role for POST/DELETE and viewer role for GET
6. WHEN providing auth endpoints THEN the system SHALL include /auth/token, /auth/refresh, and /auth/me

### Requirement 5: Protected API Routes

**User Story:** As a security officer, I want all sensitive endpoints protected, so that unauthorized users cannot access predictions or explanations.

#### Acceptance Criteria

1. WHEN accessing prediction endpoints THEN the system SHALL require valid JWT authentication
2. WHEN accessing explain endpoints THEN the system SHALL require valid JWT authentication
3. WHEN accessing system decision endpoint THEN the system SHALL allow viewer role or higher
4. WHEN authentication fails THEN the system SHALL return 401 Unauthorized
5. WHEN authorization fails THEN the system SHALL return 403 Forbidden

### Requirement 6: Database Persistence

**User Story:** As a system operator, I want persistent storage of metrics and decisions, so that historical data survives restarts.

#### Acceptance Criteria

1. WHEN initializing database THEN the system SHALL create SQLite database with SQLAlchemy
2. WHEN defining schema THEN the system SHALL create tables for city_metrics, emergency_events, and system_decisions
3. WHEN recording metrics THEN the system SHALL persist each state update to city_metrics table
4. WHEN recording decisions THEN the system SHALL persist each decision to system_decisions table
5. WHEN querying history THEN the system SHALL read from database instead of in-memory deque
6. WHEN setting up migrations THEN the system SHALL use Alembic for schema versioning

### Requirement 7: Historical Data API

**User Story:** As an analyst, I want to query historical data with filters, so that I can analyze trends over specific time periods.

#### Acceptance Criteria

1. WHEN querying history THEN the system SHALL accept limit, start, and end parameters
2. WHEN filtering by date THEN the system SHALL return only records within the specified ISO date range
3. WHEN limiting results THEN the system SHALL return at most the specified number of records
4. WHEN no filters are provided THEN the system SHALL return the most recent 100 records
5. WHEN the database is empty THEN the system SHALL return an empty result set

### Requirement 8: CORS and Security Configuration

**User Story:** As a DevOps engineer, I want configurable CORS and rate limiting, so that the API is secure in production.

#### Acceptance Criteria

1. WHEN configuring CORS THEN the system SHALL read allowed origins from ALLOWED_ORIGINS environment variable
2. WHEN no origins are configured THEN the system SHALL default to ["http://localhost:3000"] in development
3. WHEN rate limiting THEN the system SHALL enforce 60 requests per minute per IP using slowapi
4. WHEN logging requests THEN the system SHALL add middleware that logs all incoming requests
5. WHEN checking health THEN the system SHALL provide /health endpoint that verifies DB connection and model loading

### Requirement 9: WebSocket Real-Time Updates

**User Story:** As a dashboard user, I want real-time updates via WebSocket, so that I see changes immediately without polling.

#### Acceptance Criteria

1. WHEN establishing connection THEN the system SHALL provide /ws/city-updates WebSocket endpoint
2. WHEN broadcasting updates THEN the system SHALL send city state to all connected clients every 5 seconds
3. WHEN connection fails THEN the system SHALL handle disconnections gracefully
4. WHEN multiple clients connect THEN the system SHALL maintain separate connections for each client
5. WHEN no clients are connected THEN the system SHALL continue simulation without broadcasting

### Requirement 10: Frontend Authentication

**User Story:** As a user, I want to log in securely, so that I can access the dashboard with proper credentials.

#### Acceptance Criteria

1. WHEN visiting /login THEN the system SHALL display a username/password form
2. WHEN submitting credentials THEN the system SHALL store JWT in httpOnly cookie via Next.js API route
3. WHEN making API calls THEN the system SHALL attach Bearer token to every request via axios interceptor
4. WHEN receiving 401 THEN the system SHALL redirect to /login page
5. WHEN logged in THEN the system SHALL display username in navbar

### Requirement 11: WebSocket Frontend Integration

**User Story:** As a dashboard user, I want automatic real-time updates, so that I don't need to manually refresh.

#### Acceptance Criteria

1. WHEN loading dashboard THEN the system SHALL establish WebSocket connection to /ws/city-updates
2. WHEN receiving updates THEN the system SHALL update dashboard state without full page reload
3. WHEN connection drops THEN the system SHALL display disconnected status in navbar
4. WHEN connection fails THEN the system SHALL fall back to 3-second polling
5. WHEN reconnecting THEN the system SHALL automatically re-establish WebSocket connection

### Requirement 12: Model Performance Dashboard

**User Story:** As a stakeholder, I want to see model performance metrics, so that I can trust the AI predictions.

#### Acceptance Criteria

1. WHEN visiting /model-stats THEN the system SHALL display accuracy, precision, recall, and F1 for each model
2. WHEN showing feature importance THEN the system SHALL display bar charts using recharts
3. WHEN showing confusion matrices THEN the system SHALL display heatmap for each model
4. WHEN loading performance data THEN the system SHALL fetch from GET /models/stats API endpoint
5. WHEN models are not loaded THEN the system SHALL display appropriate fallback message

### Requirement 13: Enhanced KPI Cards

**User Story:** As a dashboard user, I want richer KPI visualizations, so that I can quickly understand trends and thresholds.

#### Acceptance Criteria

1. WHEN displaying KPI THEN the system SHALL show sparkline of last 10 readings
2. WHEN value exceeds 80% THEN the system SHALL display animated pulse indicator
3. WHEN clicking KPI card THEN the system SHALL expand to show full historical chart
4. WHEN collapsing card THEN the system SHALL return to compact view
5. WHEN no historical data exists THEN the system SHALL display current value only

### Requirement 14: Interactive Prediction Panel

**User Story:** As a demo presenter, I want to manually input parameters and see live predictions, so that I can demonstrate the ML models interactively.

#### Acceptance Criteria

1. WHEN displaying prediction panel THEN the system SHALL show forms for traffic and waste parameters
2. WHEN submitting traffic parameters THEN the system SHALL call ML model and display prediction
3. WHEN submitting waste parameters THEN the system SHALL call ML model and display prediction
4. WHEN prediction completes THEN the system SHALL automatically display SHAP explanation
5. WHEN form is invalid THEN the system SHALL display validation errors

### Requirement 15: Enhanced Map Visualization

**User Story:** As a city planner, I want an accurate map with real coordinates, so that I can see actual junction locations.

#### Acceptance Criteria

1. WHEN displaying map THEN the system SHALL use real Udaipur junction coordinates from traffic_data.csv
2. WHEN coloring markers THEN the system SHALL use actual model predictions (not traffic_intensity string)
3. WHEN clicking marker THEN the system SHALL display full zone details and predictions
4. WHEN toggling heatmap THEN the system SHALL show/hide heatmap layer
5. WHEN no data is available THEN the system SHALL display map with default markers

### Requirement 16: API Documentation

**User Story:** As an API consumer, I want comprehensive OpenAPI documentation, so that I can integrate with the system easily.

#### Acceptance Criteria

1. WHEN viewing /api/docs THEN the system SHALL display complete OpenAPI documentation
2. WHEN documenting endpoints THEN the system SHALL include response_model and example values
3. WHEN organizing routes THEN the system SHALL use tags and descriptions for every route
4. WHEN testing endpoints THEN the system SHALL provide interactive try-it-out functionality
5. WHEN viewing schemas THEN the system SHALL display all Pydantic models with field descriptions

### Requirement 17: End-to-End Demo Script

**User Story:** As a QA engineer, I want an automated demo script, so that I can verify the entire system works end-to-end.

#### Acceptance Criteria

1. WHEN running demo script THEN the system SHALL authenticate and obtain valid JWT token
2. WHEN testing endpoints THEN the system SHALL call every API endpoint in sequence
3. WHEN displaying results THEN the system SHALL print formatted output for each response
4. WHEN any endpoint fails THEN the system SHALL report the failure clearly
5. WHEN script completes THEN the system SHALL provide summary of passed/failed tests

### Requirement 18: Comprehensive Documentation

**User Story:** As a new developer, I want clear documentation, so that I can understand and contribute to the project.

#### Acceptance Criteria

1. WHEN reading README THEN the system SHALL include architecture diagram in ASCII or Mermaid
2. WHEN following setup THEN the system SHALL provide step-by-step instructions for backend and frontend
3. WHEN understanding ML pipeline THEN the system SHALL explain how model training and prediction works
4. WHEN retraining models THEN the system SHALL document the retraining process
5. WHEN viewing API reference THEN the system SHALL include endpoint table with methods, paths, and descriptions

### Requirement 19: Docker Deployment

**User Story:** As a DevOps engineer, I want Docker configuration, so that I can deploy the system consistently across environments.

#### Acceptance Criteria

1. WHEN building backend THEN the system SHALL use Dockerfile with Python 3.11 base image
2. WHEN orchestrating services THEN the system SHALL use docker-compose.yml for backend and frontend
3. WHEN configuring environment THEN the system SHALL provide .env.example with all required variables
4. WHEN installing dependencies THEN the system SHALL use requirements.txt with pinned versions
5. WHEN running containers THEN the system SHALL expose appropriate ports and handle networking

### Requirement 20: Environment Configuration

**User Story:** As a system administrator, I want environment variable templates, so that I can configure the system without exposing secrets.

#### Acceptance Criteria

1. WHEN providing backend config THEN the system SHALL include .env.example with SECRET_KEY, ALLOWED_ORIGINS, DATABASE_URL
2. WHEN providing frontend config THEN the system SHALL include .env.local.example with NEXT_PUBLIC_API_URL
3. WHEN documenting variables THEN the system SHALL include comments explaining each variable's purpose
4. WHEN setting defaults THEN the system SHALL use safe development defaults (not production secrets)
5. WHEN deploying THEN the system SHALL validate that all required environment variables are set
