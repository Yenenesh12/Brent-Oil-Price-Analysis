"""
FAST VERSION - Bayesian Change Point Analysis
Optimized for quick execution (5-10 minutes instead of hours)
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

sys.path.append('src')
from data_loader import BrentDataLoader, EventDataLoader
from changepoint_model import BayesianChangePointModel
from event_correlator import EventCorrelator

def main():
    print("="*80)
    print("FAST BAYESIAN CHANGE POINT ANALYSIS")
    print("="*80)
    
    # Create directories
    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/data", exist_ok=True)
    
    # 1. Load data
    print("\n[1/5] Loading data...")
    loader = BrentDataLoader(data_path='data/events/BrentOilPrices.csv')
    df = loader.load_data()
    df = loader.preprocess()
    
    data = df['Log_Returns'].dropna().values
    dates = df['Date'].iloc[1:].values
    
    print(f"✓ Loaded {len(data)} data points")
    
    # 2. Build model
    print("\n[2/5] Building model...")
    n_changepoints = 3
    model = BayesianChangePointModel(data, n_changepoints=n_changepoints)
    model.build_model()
    print(f"✓ Model built with {n_changepoints} change points")
    
    # 3. FAST SAMPLING - Reduced iterations, single chain
    print("\n[3/5] Running FAST MCMC sampling...")
    print("  Using reduced iterations for speed (300 draws, 300 tune)")
    print("  This should take 3-5 minutes...")
    
    trace = model.fit(
        draws=300,      # Further reduced for speed
        tune=300,       # Further reduced for speed
        chains=1,       # Single chain (Windows compatible)
        cores=1,        # Single core to avoid overhead
        random_seed=42
    )
    print("✓ MCMC sampling complete")
    
    # 4. Extract results
    print("\n[4/5] Extracting results...")
    tau_samples = trace.posterior['tau'].values.reshape(-1, n_changepoints)
    tau_mean = tau_samples.mean(axis=0).astype(int)
    
    print("\n=== DETECTED CHANGE POINTS ===")
    changepoint_results = []
    for i, idx in enumerate(tau_mean, 1):
        date = pd.to_datetime(dates[idx])
        lower = int(np.percentile(tau_samples[:, i-1], 2.5))
        upper = int(np.percentile(tau_samples[:, i-1], 97.5))
        
        print(f"\nChange Point {i}:")
        print(f"  Date: {date.strftime('%Y-%m-%d')}")
        print(f"  95% CI: {pd.to_datetime(dates[lower]).strftime('%Y-%m-%d')} to {pd.to_datetime(dates[upper]).strftime('%Y-%m-%d')}")
        
        changepoint_results.append({
            'changepoint_id': i,
            'index': idx,
            'date': date,
            'lower_ci': pd.to_datetime(dates[lower]),
            'upper_ci': pd.to_datetime(dates[upper])
        })
    
    # Save results
    cp_df = pd.DataFrame(changepoint_results)
    cp_df.to_csv('outputs/data/changepoint_results.csv', index=False)
    print("\n✓ Results saved")
    
    # 5. Event correlation
    print("\n[5/5] Event correlation...")
    event_loader = EventDataLoader(events_path='data/events/geopolitical_events.csv')
    events_df = event_loader.load_events()
    
    correlator = EventCorrelator(events_df, pd.Series(dates))
    correlation_results = correlator.correlate_changepoints(tau_mean, window_days=60)
    
    all_correlations = []
    for result in correlation_results:
        cp_date = result['changepoint_date']
        print(f"\nChange Point: {cp_date.strftime('%Y-%m-%d')}")
        
        if result['events']:
            print(f"  Found {len(result['events'])} nearby events")
            for event in result['events'][:3]:
                all_correlations.append({
                    'changepoint_date': cp_date,
                    'event_date': event['event_date'],
                    'event_description': event['description'],
                    'event_category': event['category'],
                    'days_difference': event['days_difference'],
                    'proximity_score': event['proximity_score']
                })
    
    if all_correlations:
        corr_df = pd.DataFrame(all_correlations)
        corr_df.to_csv('outputs/data/event_correlations.csv', index=False)
    
    # Generate plots
    print("\nGenerating visualizations...")
    fig = model.plot_trace()
    plt.savefig("outputs/figures/trace_plots.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    fig = model.plot_results(dates=dates, figsize=(18, 10))
    plt.savefig("outputs/figures/changepoint_results.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save processed data
    dashboard_data = df[['Date', 'Price', 'Returns', 'Log_Returns']].copy()
    dashboard_data.to_csv('outputs/data/processed_prices.csv', index=False)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  • outputs/data/changepoint_results.csv")
    print("  • outputs/data/event_correlations.csv")
    print("  • outputs/data/processed_prices.csv")
    print("  • outputs/figures/trace_plots.png")
    print("  • outputs/figures/changepoint_results.png")
    print("\nNote: This used reduced iterations for speed.")
    print("For production, increase draws to 2000 and tune to 1000.")

if __name__ == '__main__':
    main()
