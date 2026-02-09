# Brent Oil Price Analysis

## Project Overview
This project analyzes Brent crude oil price fluctuations using Bayesian change point detection models to identify structural breaks and their correlation with major geopolitical and economic events.

**Organization:** Birhan Energies  
**Objective:** Data-driven decision-making in the energy market through statistical analysis of oil price dynamics.

## Key Features

✅ **Bayesian Change Point Detection** - Identify structural breaks in price series  
✅ **Event Correlation Analysis** - Link price changes to geopolitical events  
✅ **Time Series Analysis** - Stationarity testing, volatility analysis, trend decomposition  
✅ **Interactive Dashboard** - Flask + React web application for data exploration  
✅ **Comprehensive Documentation** - Analysis workflow, methodology, and limitations

## Project Structure
```
Brent-Oil-Price-Analysis/
├── data/
│   └── events/
│       ├── BrentOilPrices.csv           # Historical price data
│       └── geopolitical_events.csv      # Curated events dataset
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb    # EDA and data exploration
│   ├── 02_time_series_properties.ipynb  # Stationarity and volatility
│   └── 03_changepoint_analysis.ipynb    # Bayesian modeling
├── src/
│   ├── data_loader.py                   # Data loading utilities
│   ├── time_series_analysis.py          # Time series functions
│   ├── changepoint_model.py             # Bayesian model implementation
│   └── event_correlator.py              # Event correlation logic
├── dashboard/
│   ├── backend/                         # Flask REST API
│   └── frontend/                        # React application
├── outputs/
│   ├── data/                            # Analysis results (CSV)
│   └── figures/                         # Visualizations (PNG)
├── docs/
│   ├── analysis_workflow.md             # Detailed methodology
│   └── task2_task3_requirements.html    # Project requirements
├── run_changepoint_analysis.py          # Main analysis script
├── requirements.txt                     # Python dependencies
└── README.md
```

## Quick Start

### 1. Installation

```bash
<<<<<<< task-2-3
# Clone the repository
git clone <repository-url>
=======
git clone <(https://github.com/Yenenesh12/Brent-Oil-Price-Analysis.git)>
>>>>>>> main
cd Brent-Oil-Price-Analysis

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Git Bash on Windows
# OR
venv\Scripts\activate  # CMD on Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Analysis

```bash
# Execute Bayesian change point analysis
python run_changepoint_analysis.py
```

This will:
- Load and preprocess Brent oil price data
- Build and fit Bayesian change point model
- Detect structural breaks in the price series
- Correlate change points with geopolitical events
- Generate visualizations and save results to `outputs/`

**Expected runtime:** 5-10 minutes

### 3. Launch the Dashboard

**Backend:**
```bash
cd dashboard/backend
pip install -r requirements.txt
python app.py
```

**Frontend (new terminal):**
```bash
cd dashboard/frontend
npm install
npm start
```

Access the dashboard at `http://localhost:3000`

## Analysis Workflow

### Phase 1: Data Preparation
- Load historical Brent oil prices (1987-2022)
- Compile geopolitical events dataset
- Clean and preprocess data
- Calculate returns and log returns

### Phase 2: Exploratory Analysis
- Descriptive statistics
- Trend analysis with moving averages
- Stationarity testing (ADF, KPSS)
- Volatility patterns
- Autocorrelation analysis

### Phase 3: Bayesian Change Point Detection
- Build PyMC model with discrete change points
- Define priors for change point locations and segment means
- Run MCMC sampling (NUTS algorithm)
- Check convergence diagnostics (R-hat, trace plots)
- Extract posterior distributions

### Phase 4: Event Correlation
- Temporal alignment of change points with events
- Proximity scoring (±60 day window)
- Category-based relevance weighting
- Statistical correlation analysis

### Phase 5: Visualization & Reporting
- Interactive dashboard with multiple views
- Change point visualizations
- Event timeline with correlations
- Summary statistics and insights

## Key Technologies

**Analysis:**
- Python 3.8+
- pandas, numpy - Data manipulation
- PyMC - Bayesian modeling
- ArviZ - Bayesian diagnostics
- statsmodels - Time series analysis
- matplotlib, seaborn - Visualization

**Dashboard:**
- Flask - REST API backend
- React - Frontend framework
- Recharts - Interactive charts
- Axios - HTTP client

## Results

The analysis identifies **3 major change points** in Brent oil prices, corresponding to:
1. Major geopolitical events (wars, conflicts)
2. OPEC policy decisions
3. Economic crises and supply disruptions

Results are saved in `outputs/data/`:
- `changepoint_results.csv` - Detected change points with confidence intervals
- `event_correlations.csv` - Event-changepoint correlations with proximity scores
- `processed_prices.csv` - Cleaned price data with returns

Visualizations in `outputs/figures/`:
- `changepoint_results.png` - Price series with detected change points
- `trace_plots.png` - MCMC convergence diagnostics

## Dashboard Features

📊 **Price History Chart** - Interactive visualization with change points  
📈 **Volatility Analysis** - Rolling volatility with adjustable windows  
📅 **Event Timeline** - Filterable events with correlation scores  
📉 **Statistics Dashboard** - Key metrics and summary statistics  
🔍 **Date Range Filter** - Custom time period selection

## Methodology

### Bayesian Change Point Model

**Model Specification:**
```
τ ~ DiscreteUniform(0, n-1)              # Change point locations
μ ~ Normal(data_mean, 2*data_std)        # Segment means
σ ~ HalfNormal(data_std)                 # Observation noise
obs ~ Normal(μ[segment(τ)], σ)           # Likelihood
```

**Inference:**
- MCMC sampling using No-U-Turn Sampler (NUTS)
- 2000 draws, 1000 tuning steps
- Convergence assessed via R-hat and effective sample size

### Event Correlation

**Proximity Score:**
```
score = 1 - (|days_difference| / max_window)
```

Where `max_window = 60 days` (±2 months)

**Relevance Weighting:**
- War/Conflict: 1.5x
- Supply Disruption: 1.3x
- Policy Decision: 1.2x
- Demand Shock: 1.1x
- Economic Event: 1.0x

## Limitations

### Data Limitations
- Daily frequency may miss intraday volatility
- Weekend/holiday gaps in data
- Historical data quality varies by period

### Methodological Limitations
- **Correlation ≠ Causation**: Temporal proximity doesn't prove causation
- Discrete change points may miss gradual transitions
- Model assumes finite number of change points
- Event dataset may be incomplete

### Analytical Limitations
- Historical patterns may not predict future behavior
- Black swan events are unpredictable
- Multiple confounding factors may be present
- Findings specific to Brent crude

## Documentation

- `docs/analysis_workflow.md` - Comprehensive methodology and workflow
- `dashboard/README.md` - Dashboard setup and API documentation
- Jupyter notebooks - Interactive analysis with detailed comments

## Deliverables

✅ **Analysis Code** - Modular Python modules and notebooks  
✅ **Bayesian Model** - PyMC implementation with diagnostics  
✅ **Interactive Dashboard** - Flask + React web application  
✅ **Visualizations** - High-quality plots and charts  
✅ **Documentation** - Methodology, setup guides, and insights  
✅ **Data Files** - Processed data and analysis results

## Future Work

<<<<<<< task-2-3
- Extend to multiple change points with hierarchical models
- Incorporate macroeconomic indicators (GDP, inflation, exchange rates)
- VAR models for dynamic relationships
- Markov-Switching models for regime detection
- Real-time change point detection
- Predictive modeling and forecasting

## Contributing

This project is part of Birhan Energies' data science initiative. For questions or contributions, please contact the project team.

## License

© 2026 Birhan Energies. All rights reserved.

## Acknowledgments

- Energy Information Administration (EIA) for historical price data
- OPEC for market reports and policy information
- PyMC development team for excellent Bayesian modeling tools


=======

>>>>>>> main
