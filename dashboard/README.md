# Brent Oil Price Analysis Dashboard

Interactive web dashboard for exploring Bayesian change point detection results and event correlations in Brent oil prices.

## Architecture

- **Backend**: Flask REST API (Python)
- **Frontend**: React with Recharts for visualizations
- **Data**: CSV files generated from Bayesian analysis

## Project Structure

```
dashboard/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── PriceChart.js
│   │   │   ├── VolatilityChart.js
│   │   │   ├── EventTimeline.js
│   │   │   ├── Statistics.js
│   │   │   └── DateRangeFilter.js
│   │   ├── App.js          # Main application
│   │   ├── api.js          # API client
│   │   └── index.js        # Entry point
│   └── package.json        # Node dependencies
└── README.md
```

## Prerequisites

### Backend
- Python 3.8+
- pip

### Frontend
- Node.js 16+ and npm

## Installation & Setup

### Step 1: Run the Analysis (if not already done)

From the project root directory:

```bash
python run_changepoint_analysis.py
```

This generates the required data files in `outputs/data/`:
- `processed_prices.csv`
- `changepoint_results.csv`
- `event_correlations.csv`

### Step 2: Setup Backend

```bash
cd dashboard/backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows Git Bash
# OR
venv\Scripts\activate  # On Windows CMD

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The API will be available at `http://localhost:5000`

### Step 3: Setup Frontend

Open a new terminal:

```bash
cd dashboard/frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The dashboard will open automatically at `http://localhost:3000`

## API Endpoints

### GET /api/health
Health check endpoint

### GET /api/prices
Get historical price data
- Query params: `start_date`, `end_date` (optional)
- Returns: dates, prices, returns, log_returns

### GET /api/changepoints
Get detected change points
- Returns: Array of change points with dates and confidence intervals

### GET /api/events
Get geopolitical events
- Query params: `category`, `start_date`, `end_date` (optional)
- Returns: Array of events

### GET /api/correlations
Get event-changepoint correlations
- Returns: Array of correlations with proximity scores

### GET /api/statistics
Get summary statistics
- Returns: Overall statistics about the dataset

### GET /api/volatility
Get rolling volatility
- Query params: `window` (default: 30)
- Returns: dates and volatility values

## Dashboard Features

### 1. Price History Chart
- Interactive line chart showing Brent oil prices over time
- Vertical lines marking detected change points
- Hover tooltips showing price and events on specific dates
- Change point legend with confidence intervals

### 2. Volatility Analysis
- Rolling volatility chart with adjustable window size
- Options: 7, 30, 90, or 180-day windows
- Annualized volatility calculation

### 3. Event Timeline
- Filterable list of geopolitical events
- Category-based filtering (War, Policy, Economic, Supply, Demand)
- Change point correlation view
- Proximity scores showing temporal alignment

### 4. Statistics Dashboard
- Key metrics overview
- Date range, total observations
- Price statistics (mean, std, min, max)
- Change points and correlations count

### 5. Date Range Filter
- Filter all data by custom date range
- Reset functionality to view full dataset

## Development

### Backend Development

The Flask app uses CORS to allow cross-origin requests from the React frontend.

To modify API endpoints, edit `dashboard/backend/app.py`.

### Frontend Development

React components are in `dashboard/frontend/src/components/`.

To add new visualizations:
1. Create a new component in `src/components/`
2. Import and use it in `App.js`
3. Add corresponding API endpoint if needed

### Styling

Each component has its own CSS file for styling. Global styles are in `src/index.css` and `src/App.css`.

## Production Build

### Backend
```bash
# Use a production WSGI server like Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
cd dashboard/frontend
npm run build
```

The optimized production build will be in `dashboard/frontend/build/`.

Serve it with a static file server or integrate with the Flask backend.

## Troubleshooting

### Backend Issues

**Error: Data not available**
- Ensure you've run `run_changepoint_analysis.py` first
- Check that CSV files exist in `outputs/data/`

**Port 5000 already in use**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`
- Update API_BASE_URL in `frontend/src/api.js`

### Frontend Issues

**Cannot connect to API**
- Ensure Flask backend is running on port 5000
- Check browser console for CORS errors
- Verify API_BASE_URL in `src/api.js`

**npm install fails**
- Try deleting `node_modules` and `package-lock.json`
- Run `npm install` again
- Ensure Node.js version is 16+

## Screenshots

(Add screenshots of your dashboard here after running it)

## Future Enhancements

- Real-time data updates
- Export functionality for charts
- Advanced filtering options
- Regime-specific analysis
- Predictive modeling integration
- User authentication
- Saved views/bookmarks

## License

Part of the Brent Oil Price Analysis project by Birhan Energies.
