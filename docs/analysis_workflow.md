# Brent Oil Price Analysis Workflow
**Project:** Bayesian Change Point Detection for Oil Price Analysis  
**Organization:** Birhan Energies  
**Date:** February 2026

---

## 1. Data Analysis Workflow

### Phase 1: Data Collection & Preparation
**Objective:** Gather and prepare all necessary data for analysis

**Steps:**
1. **Load Brent Oil Price Data**
   - Source: Historical Brent crude oil prices (May 1987 - November 2022)
   - Format: CSV with Date and Price columns
   - Validation: Check for missing values, duplicates, and data quality issues

2. **Compile Geopolitical Events Dataset**
   - Research major events affecting oil markets (1987-2022)
   - Categories: Geopolitical conflicts, OPEC decisions, economic crises, supply disruptions
   - Structure: CSV with columns: Date, Event, Category, Description

3. **Data Cleaning**
   - Handle missing values (interpolation or forward-fill for small gaps)
   - Convert date formats to datetime objects
   - Remove outliers or flag anomalies for investigation
   - Ensure consistent frequency (daily data)

### Phase 2: Exploratory Data Analysis (EDA)
**Objective:** Understand data characteristics and inform modeling decisions

**Steps:**
1. **Descriptive Statistics**
   - Calculate mean, median, standard deviation, min/max prices
   - Identify price ranges across different time periods
   - Compute returns and volatility metrics

2. **Trend Analysis**
   - Visual inspection using line plots
   - Moving averages (30-day, 90-day, 365-day)
   - Decomposition into trend, seasonal, and residual components

3. **Stationarity Testing**
   - Augmented Dickey-Fuller (ADF) test
   - Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test
   - Phillips-Perron test
   - Interpretation: Determine if differencing is needed

4. **Volatility Analysis**
   - Rolling standard deviation
   - Identify periods of high/low volatility
   - GARCH modeling considerations

5. **Autocorrelation Analysis**
   - ACF and PACF plots
   - Identify temporal dependencies

### Phase 3: Change Point Detection
**Objective:** Identify structural breaks in the price series using Bayesian methods

**Steps:**
1. **Model Selection**
   - Choose appropriate change point model (mean shift, variance shift, or both)
   - Define prior distributions for parameters
   - Set number of potential change points

2. **Bayesian Model Implementation (PyMC)**
   - Define likelihood function
   - Specify priors for change point locations and parameters
   - Configure MCMC sampling (NUTS sampler)
   - Run inference with sufficient iterations (2000-5000 samples)

3. **Model Diagnostics**
   - Trace plots for convergence assessment
   - R-hat statistics (should be < 1.01)
   - Effective sample size
   - Posterior predictive checks

4. **Extract Change Points**
   - Identify most probable change point dates
   - Estimate parameter values before/after each change point
   - Calculate credible intervals (95% HDI)

### Phase 4: Event Correlation Analysis
**Objective:** Investigate relationships between detected change points and historical events

**Steps:**
1. **Temporal Alignment**
   - Match change points with events within ±30 day window
   - Create visualization overlaying events on price series

2. **Statistical Correlation**
   - Calculate correlation coefficients
   - Perform significance tests
   - Document correlation vs. causation distinction

3. **Qualitative Analysis**
   - Interpret economic/geopolitical context
   - Assess plausibility of causal relationships

### Phase 5: Insight Generation & Reporting
**Objective:** Communicate findings to stakeholders

**Steps:**
1. **Synthesize Findings**
   - Summarize key change points and their magnitudes
   - Highlight significant event correlations
   - Identify patterns and trends

2. **Create Visualizations**
   - Time series plots with change points marked
   - Event timeline overlays
   - Posterior distribution plots
   - Volatility regime charts

3. **Document Limitations**
   - Model assumptions and their validity
   - Data quality issues
   - Correlation vs. causation caveats

4. **Prepare Deliverables**
   - Executive summary (1-2 pages)
   - Technical report with methodology
   - Jupyter notebooks with reproducible analysis
   - Presentation slides for stakeholders

---

## 2. Assumptions and Limitations

### Assumptions
1. **Data Quality:** Historical price data is accurate and representative of actual market conditions
2. **Market Efficiency:** Prices reflect available information, though with potential lags
3. **Event Impact:** Major geopolitical/economic events can cause structural breaks in price dynamics
4. **Model Assumptions:**
   - Price changes follow a piecewise stationary process
   - Change points are discrete and identifiable
   - Prior distributions reasonably represent our uncertainty

### Limitations

#### Data Limitations
- **Missing Data:** Gaps in historical records may exist (weekends, holidays)
- **Data Frequency:** Daily data may miss intraday volatility
- **Price Source:** Different pricing benchmarks (spot vs. futures) may vary

#### Methodological Limitations
- **Change Point Detection:**
  - Model assumes finite number of change points
  - May miss gradual transitions
  - Sensitive to prior specifications
  - Computational intensity limits model complexity

- **Event Dataset:**
  - Event selection is subjective
  - Event dates may be approximate (gradual developments)
  - Incomplete coverage of all market-moving factors
  - Difficult to quantify event "magnitude"

#### Analytical Limitations
- **Correlation ≠ Causation:**
  - **CRITICAL DISTINCTION:** Finding that a change point occurs near an event date does NOT prove the event caused the price change
  - Temporal correlation is necessary but not sufficient for causation
  - Multiple confounding factors may be present
  - Reverse causality is possible (oil prices affecting geopolitical events)
  - Third variables may drive both events and prices
  - **Establishing Causation Requires:**
    - Controlled experiments (impossible in macroeconomics)
    - Instrumental variables or natural experiments
    - Detailed mechanism analysis
    - Ruling out alternative explanations

- **Forecasting:**
  - Historical patterns may not predict future behavior
  - Black swan events are unpredictable
  - Model does not account for structural changes in global energy markets

- **External Validity:**
  - Findings specific to Brent crude; may not generalize to other commodities
  - Historical relationships may change over time

---

## 3. Communication Channels

### Primary Stakeholders
1. **Executive Leadership** - Strategic decision-making
2. **Trading/Operations Teams** - Tactical implementation
3. **Risk Management** - Portfolio optimization
4. **Research Team** - Methodology validation

### Communication Formats

#### 1. Executive Dashboard
- **Medium:** Interactive web dashboard (Plotly/Dash)
- **Content:** Key metrics, visualizations, high-level insights
- **Frequency:** Updated quarterly or on-demand
- **Audience:** C-suite, senior management

#### 2. Technical Reports
- **Medium:** PDF documents with detailed methodology
- **Content:** Full analysis workflow, statistical tests, model diagnostics
- **Frequency:** Major analysis milestones
- **Audience:** Data science team, quantitative analysts

#### 3. Jupyter Notebooks
- **Medium:** GitHub repository with documented code
- **Content:** Reproducible analysis, code, visualizations
- **Frequency:** Continuous updates
- **Audience:** Technical team members, peer reviewers

#### 4. Presentation Slides
- **Medium:** PowerPoint/Google Slides
- **Content:** Key findings, visualizations, recommendations
- **Frequency:** Quarterly business reviews, ad-hoc meetings
- **Audience:** Cross-functional teams, stakeholders

#### 5. Email Summaries
- **Medium:** Email with embedded charts
- **Content:** Brief updates on significant findings
- **Frequency:** As needed for urgent insights
- **Audience:** Relevant decision-makers

#### 6. Team Meetings
- **Medium:** In-person or virtual presentations
- **Content:** Interactive discussion of findings and implications
- **Frequency:** Bi-weekly or monthly
- **Audience:** Project team, collaborators

---

## 4. Understanding Change Point Models

### What are Change Point Models?

Change point models are statistical methods designed to identify points in time where the statistical properties of a time series undergo significant changes. In the context of oil price analysis, these models help detect when price dynamics shift due to structural breaks in the market.

### Purpose in Oil Price Analysis

1. **Identify Regime Changes:** Detect transitions between different market conditions (e.g., stable → volatile)
2. **Structural Break Detection:** Find points where price behavior fundamentally changes
3. **Event Impact Assessment:** Quantify when and how external shocks affect prices
4. **Risk Management:** Understand volatility regimes for better hedging strategies
5. **Market Segmentation:** Divide historical data into homogeneous periods for analysis

### Bayesian Approach with PyMC

**Why Bayesian?**
- Incorporates prior knowledge about oil markets
- Provides full probability distributions (not just point estimates)
- Naturally handles uncertainty in change point locations
- Allows for complex hierarchical models

**PyMC Implementation:**
- Uses Markov Chain Monte Carlo (MCMC) for inference
- No-U-Turn Sampler (NUTS) for efficient sampling
- Provides credible intervals for all parameters
- Enables model comparison via information criteria

### Expected Outputs

#### 1. Change Point Locations
- **Format:** Dates with probability distributions
- **Example:** "High probability change point on August 2, 1990 (Gulf War invasion)"
- **Uncertainty:** 95% credible interval around each change point

#### 2. Parameter Estimates
- **Mean Levels:** Average price in each regime
- **Variance Changes:** Volatility in each period
- **Magnitude:** Size of price shifts at change points
- **Example:** "Mean price shifted from $18.50 to $28.30 (±$2.10)"

#### 3. Posterior Distributions
- Full probability distributions for all parameters
- Visualized as histograms or density plots
- Allows probabilistic statements about parameters

#### 4. Model Diagnostics
- Convergence metrics (R-hat, effective sample size)
- Trace plots showing MCMC sampling behavior
- Posterior predictive checks for model validation

#### 5. Visualizations
- Time series with change points marked
- Regime-specific confidence bands
- Parameter posterior distributions
- Event correlation plots

### Limitations of Change Point Analysis

1. **Discrete Assumption:** Assumes changes are abrupt, may miss gradual transitions
2. **Number of Change Points:** Must specify or estimate; too many leads to overfitting
3. **Computational Cost:** Bayesian inference can be slow for long time series
4. **Prior Sensitivity:** Results may depend on prior specifications
5. **Identification:** Difficult to distinguish between multiple closely-spaced change points
6. **Causation:** Model identifies "when" but not "why" changes occur
7. **Out-of-Sample:** Historical change points don't predict future ones

---

## 5. Time Series Properties Analysis

### Trend Analysis
**Purpose:** Identify long-term directional movements in oil prices

**Methods:**
- Visual inspection of price plots
- Linear/polynomial trend fitting
- Moving averages (MA30, MA90, MA365)
- Hodrick-Prescott filter for trend-cycle decomposition

**Implications for Modeling:**
- Strong trend → May need differencing or detrending
- Multiple trends → Suggests multiple regimes (change points)
- No trend → Stationary mean, simpler models applicable

### Stationarity Testing
**Purpose:** Determine if statistical properties are constant over time

**Tests:**
1. **Augmented Dickey-Fuller (ADF)**
   - Null hypothesis: Unit root present (non-stationary)
   - p-value < 0.05 → Reject null, series is stationary

2. **KPSS Test**
   - Null hypothesis: Series is stationary
   - p-value < 0.05 → Reject null, series is non-stationary

3. **Phillips-Perron Test**
   - Similar to ADF but robust to heteroskedasticity

**Implications for Modeling:**
- Non-stationary → Apply differencing or use models that handle trends
- Stationary → Can use standard time series models
- Change points often cause apparent non-stationarity

### Volatility Patterns
**Purpose:** Understand price variability over time

**Metrics:**
- Rolling standard deviation (30-day, 90-day windows)
- Coefficient of variation
- Range-based volatility estimators

**Patterns to Identify:**
- Volatility clustering (high volatility periods cluster together)
- Regime-dependent volatility (different volatility in different periods)
- Asymmetric volatility (larger moves during crises)

**Implications for Modeling:**
- Volatility clustering → GARCH-type models may be appropriate
- Regime changes → Change point models should include variance shifts
- High volatility periods → May correspond to major events

---

## 6. Key References

### Academic Papers
1. **Change Point Detection:**
   - Barry & Hartigan (1993) - "A Bayesian Analysis for Change Point Problems"
   - Chib (1998) - "Estimation and comparison of multiple change-point models"

2. **Oil Price Dynamics:**
   - Hamilton (2009) - "Causes and Consequences of the Oil Shock of 2007-08"
   - Kilian (2009) - "Not All Oil Price Shocks Are Alike"

3. **Bayesian Time Series:**
   - Carlin et al. (1992) - "Hierarchical Bayesian Analysis of Changepoint Problems"

### Technical Resources
1. **PyMC Documentation:** https://www.pymc.io/
2. **Statsmodels Time Series:** https://www.statsmodels.org/stable/tsa.html
3. **Bayesian Methods for Hackers:** Cameron Davidson-Pilon

### Domain Knowledge
1. **EIA (Energy Information Administration):** Oil market reports
2. **OPEC:** Production decisions and market analysis
3. **IEA (International Energy Agency):** Global energy outlook

---

## Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Data Preparation | Week 1 | Clean datasets, event compilation |
| EDA & Properties Analysis | Week 1-2 | Statistical summaries, stationarity tests |
| Change Point Modeling | Week 2-3 | Bayesian model, change point estimates |
| Event Correlation | Week 3 | Correlation analysis, visualizations |
| Reporting | Week 4 | Final report, presentation, notebooks |

---

## Success Criteria

1. **Data Quality:** < 1% missing data, all events documented
2. **Model Performance:** R-hat < 1.01, ESS > 1000 for all parameters
3. **Interpretability:** Clear identification of major change points
4. **Reproducibility:** All analysis documented in version-controlled notebooks
5. **Stakeholder Value:** Actionable insights for decision-making
