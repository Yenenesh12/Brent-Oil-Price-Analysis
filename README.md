# Brent Oil Price Analysis

## Project Overview
This project analyzes Brent crude oil price fluctuations using Bayesian change point detection models to identify structural breaks and their correlation with major geopolitical and economic events.

**Organization:** Birhan Energies  
**Objective:** Data-driven decision-making in the energy market through statistical analysis of oil price dynamics.

## Project Structure
```
Brent-Oil-Price-Analysis/
├── data/
│   ├── raw/                    # Raw Brent oil price data
│   ├── processed/              # Cleaned and processed data
│   └── events/                 # Geopolitical and economic events dataset
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_time_series_properties.ipynb
│   └── 03_changepoint_analysis.ipynb
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── time_series_analysis.py
│   └── changepoint_model.py
├── docs/
│   └── analysis_workflow.md
├── results/
│   ├── figures/
│   └── reports/
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Brent-Oil-Price-Analysis
```

2. Activate virtual environment:
```bash
source venv/Scripts/activate  # Git Bash
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Analysis Workflow

1. **Data Collection & Preparation**
   - Load Brent oil price historical data
   - Compile geopolitical and economic events dataset
   - Clean and preprocess data

2. **Exploratory Data Analysis**
   - Trend analysis
   - Stationarity testing (ADF, KPSS tests)
   - Volatility pattern investigation
   - Descriptive statistics

3. **Change Point Detection**
   - Bayesian change point model using PyMC
   - Identify structural breaks in price series
   - Estimate change point locations and magnitudes

4. **Event Correlation Analysis**
   - Align detected change points with historical events
   - Statistical correlation analysis
   - Visualization of relationships

5. **Insight Generation & Reporting**
   - Interpret findings
   - Document limitations
   - Communicate results to stakeholders

## Key Technologies

- **Python 3.x**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **PyMC** - Bayesian modeling
- **matplotlib/seaborn** - Visualization
- **statsmodels** - Time series analysis

## Deliverables

- Analysis workflow documentation
- Geopolitical events dataset (CSV)
- Time series analysis notebooks
- Change point detection model
- Final report with insights and limitations

## Contributors

[Your Name]

## License

[License Type]
