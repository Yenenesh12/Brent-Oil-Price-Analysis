"""
Create sample changepoint and correlation results for dashboard testing
Based on historical analysis of Brent oil prices
"""

import pandas as pd
from datetime import datetime

# Create sample changepoint results based on known historical events
changepoints = [
    {
        'changepoint_id': 1,
        'index': 850,
        'date': '1990-08-02',  # Gulf War
        'lower_ci': '1990-07-15',
        'upper_ci': '1990-08-20'
    },
    {
        'changepoint_id': 2,
        'index': 4200,
        'date': '2003-03-20',  # Iraq War
        'lower_ci': '2003-03-01',
        'upper_ci': '2003-04-10'
    },
    {
        'changepoint_id': 3,
        'index': 5500,
        'date': '2008-09-15',  # Financial Crisis
        'lower_ci': '2008-08-25',
        'upper_ci': '2008-10-05'
    }
]

cp_df = pd.DataFrame(changepoints)
cp_df.to_csv('outputs/data/changepoint_results.csv', index=False)
print("✓ Created changepoint_results.csv")

# Create sample event correlations
correlations = [
    # Gulf War correlations
    {
        'changepoint_date': '1990-08-02',
        'event_date': '1990-08-02',
        'event_description': 'Iraq invasion of Kuwait',
        'event_category': 'War',
        'days_difference': 0,
        'proximity_score': 1.0
    },
    {
        'changepoint_date': '1990-08-02',
        'event_date': '1990-08-06',
        'event_description': 'UN Security Council Resolution 661 (sanctions on Iraq)',
        'event_category': 'Policy',
        'days_difference': 4,
        'proximity_score': 0.93
    },
    # Iraq War correlations
    {
        'changepoint_date': '2003-03-20',
        'event_date': '2003-03-20',
        'event_description': 'US-led invasion of Iraq begins',
        'event_category': 'War',
        'days_difference': 0,
        'proximity_score': 1.0
    },
    {
        'changepoint_date': '2003-03-20',
        'event_date': '2003-03-17',
        'event_description': 'President Bush ultimatum to Saddam Hussein',
        'event_category': 'Policy',
        'days_difference': -3,
        'proximity_score': 0.95
    },
    # Financial Crisis correlations
    {
        'changepoint_date': '2008-09-15',
        'event_date': '2008-09-15',
        'event_description': 'Lehman Brothers files for bankruptcy',
        'event_category': 'Economic',
        'days_difference': 0,
        'proximity_score': 1.0
    },
    {
        'changepoint_date': '2008-09-15',
        'event_date': '2008-09-07',
        'event_description': 'US government takes over Fannie Mae and Freddie Mac',
        'event_category': 'Economic',
        'days_difference': -8,
        'proximity_score': 0.87
    },
    {
        'changepoint_date': '2008-09-15',
        'event_date': '2008-09-16',
        'event_description': 'AIG bailout announced',
        'event_category': 'Economic',
        'days_difference': 1,
        'proximity_score': 0.98
    }
]

corr_df = pd.DataFrame(correlations)
corr_df.to_csv('outputs/data/event_correlations.csv', index=False)
print("✓ Created event_correlations.csv")

print("\n" + "="*60)
print("Sample results created successfully!")
print("="*60)
print("\nYou can now run the dashboard:")
print("1. Backend: cd dashboard/backend && python app.py")
print("2. Frontend: cd dashboard/frontend && npm start")
print("\nNote: These are sample results based on historical analysis.")
print("Run the full Bayesian analysis later for actual results.")
