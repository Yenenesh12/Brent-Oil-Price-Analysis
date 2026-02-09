"""
Execute Bayesian Change Point Analysis
This script runs the complete analysis and saves results.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az
import warnings
warnings.filterwarnings('ignore')

sys.path.append('src')
from data_loader import BrentDataLoader, EventDataLoader
from changepoint_model import BayesianChangePointModel
from event_correlator import EventCorrelator

def main():
    # Create output directories
    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/models", exist_ok=True)
    os.makedirs("outputs/data", exist_ok=True)

    sns.set_style('whitegrid')
    np.random.seed(42)

    print("="*80)
    print("BAYESIAN CHANGE POINT ANALYSIS FOR BRENT OIL PRICES")
    print("="*80)

    # 1. Load and prepare data
    print("\n[1/6] Loading data...")
    loader = BrentDataLoader(data_path='data/events/BrentOilPrices.csv')
    df = loader.load_data()
    df = loader.preprocess()

    data = df['Log_Returns'].dropna().values
    dates = df['Date'].iloc[1:].values

    print(f"✓ Loaded {len(data)} data points")
    print(f"  Date range: {dates[0]} to {dates[-1]}")
    print(f"  Mean: {data.mean():.6f}, Std: {data.std():.6f}")

    # 2. Build model
    print("\n[2/6] Building Bayesian change point model...")
    n_changepoints = 3
    model = BayesianChangePointModel(data, n_changepoints=n_changepoints)
    model.build_model()
    print(f"✓ Model built with {n_changepoints} change points")

    # 3. Fit model (MCMC sampling) - use single chain for Windows
    print("\n[3/6] Running MCMC sampling...")
    print("  This may take 5-10 minutes...")
    trace = model.fit(draws=2000, tune=1000, chains=1, random_seed=42)
    print("✓ MCMC sampling complete")

    # 4. Check convergence
    print("\n[4/6] Checking convergence diagnostics...")
    summary = model.get_changepoint_summary()
    print("\nParameter Summary:")
    print(summary)

    # 5. Extract and save results
    print("\n[5/6] Extracting change point results...")
    tau_samples = trace.posterior['tau'].values.reshape(-1, n_changepoints)
    tau_mean = tau_samples.mean(axis=0).astype(int)
    mu_samples = trace.posterior['mu'].values.reshape(-1, n_changepoints + 1)
    mu_mean = mu_samples.mean(axis=0)

    print("\n=== DETECTED CHANGE POINTS ===")
    changepoint_results = []
    for i, idx in enumerate(tau_mean, 1):
        date = pd.to_datetime(dates[idx])
        lower = int(np.percentile(tau_samples[:, i-1], 2.5))
        upper = int(np.percentile(tau_samples[:, i-1], 97.5))
        
        print(f"\nChange Point {i}:")
        print(f"  Date: {date.strftime('%Y-%m-%d')}")
        print(f"  Index: {idx}")
        print(f"  95% CI: {pd.to_datetime(dates[lower]).strftime('%Y-%m-%d')} to {pd.to_datetime(dates[upper]).strftime('%Y-%m-%d')}")
        
        changepoint_results.append({
            'changepoint_id': i,
            'index': idx,
            'date': date,
            'lower_ci': pd.to_datetime(dates[lower]),
            'upper_ci': pd.to_datetime(dates[upper])
        })

    # Save changepoint results
    cp_df = pd.DataFrame(changepoint_results)
    cp_df.to_csv('outputs/data/changepoint_results.csv', index=False)
    print("\n✓ Change point results saved to outputs/data/changepoint_results.csv")

    # 6. Event correlation
    print("\n[6/6] Correlating with geopolitical events...")
    event_loader = EventDataLoader(events_path='data/events/geopolitical_events.csv')
    events_df = event_loader.load_events()

    correlator = EventCorrelator(events_df, pd.Series(dates))
    correlation_results = correlator.correlate_changepoints(tau_mean, window_days=60)

    print("\n=== EVENT CORRELATION RESULTS ===")
    all_correlations = []
    for result in correlation_results:
        cp_date = result['changepoint_date']
        print(f"\nChange Point: {cp_date.strftime('%Y-%m-%d')}")
        
        if result['events']:
            print(f"  Found {len(result['events'])} nearby events")
            for event in result['events'][:3]:
                print(f"    • {event['description']}")
                print(f"      ({event['event_date'].strftime('%Y-%m-%d')}, {event['days_difference']} days)")
                
                all_correlations.append({
                    'changepoint_date': cp_date,
                    'event_date': event['event_date'],
                    'event_description': event['description'],
                    'event_category': event['category'],
                    'days_difference': event['days_difference'],
                    'proximity_score': event['proximity_score']
                })
        else:
            print("  No events found in time window")

    # Save correlation results
    if all_correlations:
        corr_df = pd.DataFrame(all_correlations)
        corr_df.to_csv('outputs/data/event_correlations.csv', index=False)
        print("\n✓ Event correlations saved to outputs/data/event_correlations.csv")

    # Generate visualizations
    print("\n[7/7] Generating visualizations...")

    # Trace plots
    fig = model.plot_trace()
    plt.savefig("outputs/figures/trace_plots.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Trace plots saved")

    # Change point results
    fig = model.plot_results(dates=dates, figsize=(18, 10))
    plt.savefig("outputs/figures/changepoint_results.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Change point results plot saved")

    # Save processed data for dashboard
    dashboard_data = df[['Date', 'Price', 'Returns', 'Log_Returns']].copy()
    dashboard_data.to_csv('outputs/data/processed_prices.csv', index=False)
    print("✓ Processed data saved for dashboard")

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  • outputs/data/changepoint_results.csv")
    print("  • outputs/data/event_correlations.csv")
    print("  • outputs/data/processed_prices.csv")
    print("  • outputs/figures/trace_plots.png")
    print("  • outputs/figures/changepoint_results.png")
    print("\nReady for dashboard development!")


if __name__ == '__main__':
    main()
