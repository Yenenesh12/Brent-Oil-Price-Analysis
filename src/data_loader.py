"""
Data loading and preprocessing module for Brent oil price analysis.
"""

import pandas as pd
import numpy as np


class BrentDataLoader:
    """Load and preprocess Brent oil price data."""

    def __init__(self, data_path='data/events/BrentOilPrices.csv'):
        """
        Initialize data loader.

        Parameters:
        -----------
        data_path : str
            Path to Brent oil prices CSV file
        """
        self.data_path = data_path
        self.df = None

    def load_data(self):
        """Load Brent oil price data from CSV."""
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} records")
        return self.df

    def preprocess(self):
        """Clean and preprocess the data."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # ✅ Convert Date column to datetime (pandas 2.x compatible)
        self.df['Date'] = pd.to_datetime(
            self.df['Date'],
            errors='coerce'
        )

        # Drop rows with invalid dates
        self.df = self.df.dropna(subset=['Date'])

        # Sort by date
        self.df = self.df.sort_values('Date').reset_index(drop=True)

        # Check for missing price values
        missing = self.df['Price'].isna().sum()
        if missing > 0:
            print(f"Warning: {missing} missing price values found")
            self.df['Price'] = self.df['Price'].ffill()

        # Remove non-positive prices (log safety)
        self.df = self.df[self.df['Price'] > 0]

        # Calculate simple returns
        self.df['Returns'] = self.df['Price'].pct_change()

        # Calculate log returns
        self.df['Log_Returns'] = np.log(self.df['Price']).diff()

        print(
            f"Data preprocessed: "
            f"{self.df['Date'].min()} to {self.df['Date'].max()}"
        )

        return self.df

    def get_summary_stats(self):
        """Get summary statistics of the price data."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        return {
            'count': len(self.df),
            'mean': self.df['Price'].mean(),
            'median': self.df['Price'].median(),
            'std': self.df['Price'].std(),
            'min': self.df['Price'].min(),
            'max': self.df['Price'].max(),
            'start_date': self.df['Date'].min(),
            'end_date': self.df['Date'].max()
        }


class EventDataLoader:
    """Load geopolitical and economic events data."""

    def __init__(self, events_path='data/events/geopolitical_events.csv'):
        """
        Initialize event data loader.

        Parameters:
        -----------
        events_path : str
            Path to events CSV file
        """
        self.events_path = events_path
        self.events_df = None

    def load_events(self):
        """Load events data from CSV."""
        self.events_df = pd.read_csv(self.events_path)

        # Safe datetime conversion
        self.events_df['Date'] = pd.to_datetime(
            self.events_df['Date'],
            errors='coerce'
        )

        self.events_df = self.events_df.dropna(subset=['Date'])

        print(f"Loaded {len(self.events_df)} events")
        return self.events_df

    def get_events_by_category(self, category):
        """Filter events by category."""
        if self.events_df is None:
            raise ValueError("Events not loaded. Call load_events() first.")

        return self.events_df[self.events_df['Category'] == category]

    def get_events_in_range(self, start_date, end_date):
        """Get events within a date range."""
        if self.events_df is None:
            raise ValueError("Events not loaded. Call load_events() first.")

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        mask = (
            (self.events_df['Date'] >= start_date) &
            (self.events_df['Date'] <= end_date)
        )
        return self.events_df[mask]


if __name__ == "__main__":
    # Example usage
    loader = BrentDataLoader()
    df = loader.load_data()
    df = loader.preprocess()

    print("\nSummary Statistics:")
    stats = loader.get_summary_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 50)

    event_loader = EventDataLoader()
    events = event_loader.load_events()

    print("\nEvent Categories:")
    print(events['Category'].value_counts())
