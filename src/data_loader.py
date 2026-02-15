"""
Data loading and preprocessing module for Brent oil price analysis.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

import pandas as pd
import numpy as np


@dataclass
class DataSummary:
    """Dataclass for summary statistics."""
    count: int
    mean: float
    median: float
    std: float
    min_price: float
    max_price: float
    start_date: datetime
    end_date: datetime


class BrentDataLoader:
    """Load and preprocess Brent oil price data."""

    def __init__(self, data_path: str = 'data/events/BrentOilPrices.csv'):
        """
        Initialize data loader.

        Parameters:
        -----------
        data_path : str
            Path to Brent oil prices CSV file
        """
        self.data_path: str = data_path
        self.df: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """Load Brent oil price data from CSV."""
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} records")
        return self.df

    def preprocess(self) -> pd.DataFrame:
        """Clean and preprocess the data."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
        self.df = self.df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)

        missing = self.df['Price'].isna().sum()
        if missing > 0:
            print(f"Warning: {missing} missing price values found")
            self.df['Price'] = self.df['Price'].ffill()

        self.df = self.df[self.df['Price'] > 0]
        self.df['Returns'] = self.df['Price'].pct_change()
        self.df['Log_Returns'] = np.log(self.df['Price']).diff()

        print(f"Data preprocessed: {self.df['Date'].min()} to {self.df['Date'].max()}")
        return self.df

    def get_summary_stats(self) -> DataSummary:
        """Get summary statistics of the price data."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        prices = self.df['Price']
        return DataSummary(
            count=len(self.df),
            mean=float(prices.mean()),
            median=float(prices.median()),
            std=float(prices.std()),
            min_price=float(prices.min()),
            max_price=float(prices.max()),
            start_date=self.df['Date'].min(),
            end_date=self.df['Date'].max()
        )


class EventDataLoader:
    """Load geopolitical and economic events data."""

    def __init__(self, events_path: str = 'data/events/geopolitical_events.csv'):
        """
        Initialize event data loader.

        Parameters:
        -----------
        events_path : str
            Path to events CSV file
        """
        self.events_path: str = events_path
        self.events_df: Optional[pd.DataFrame] = None

    def load_events(self) -> pd.DataFrame:
        """Load events data from CSV."""
        self.events_df = pd.read_csv(self.events_path)

        self.events_df['Date'] = pd.to_datetime(self.events_df['Date'], errors='coerce')
        self.events_df = self.events_df.dropna(subset=['Date'])

        print(f"Loaded {len(self.events_df)} events")
        return self.events_df

    def get_events_by_category(self, category: str) -> pd.DataFrame:
        """Filter events by category."""
        if self.events_df is None:
            raise ValueError("Events not loaded. Call load_events() first.")

        return self.events_df[self.events_df['Category'] == category]

    def get_events_in_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
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
    print(stats)

    print("\n" + "=" * 50)

    event_loader = EventDataLoader()
    events = event_loader.load_events()

    print("\nEvent Categories:")
    print(events['Category'].value_counts())