"""
Event correlation module for linking changepoints with geopolitical events.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@dataclass
class CorrelationResult:
    """Dataclass for correlation results."""
    changepoint_index: int
    changepoint_date: datetime
    events: List[Dict[str, any]]


class EventCorrelator:
    """
    Correlate detected changepoints with geopolitical events.
    
    This class identifies events that occur near changepoints and ranks them
    by temporal proximity and category relevance.
    """
    
    def __init__(self, events_df: pd.DataFrame, dates: pd.Series):
        """
        Initialize the event correlator.
        
        Parameters:
        -----------
        events_df : pd.DataFrame
            DataFrame containing geopolitical events with columns:
            - Date: datetime
            - Event: str (event description)
            - Category: str (event category)
        dates : pd.Series or array-like
            Series of dates corresponding to the time series indices
        """
        self.events_df: pd.DataFrame = events_df.copy()
        self.dates: pd.Series = pd.Series(dates) if not isinstance(dates, pd.Series) else dates.copy()
        
        # Ensure dates are datetime objects
        if not pd.api.types.is_datetime64_any_dtype(self.events_df['Date']):
            self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
        
        if not pd.api.types.is_datetime64_any_dtype(self.dates):
            self.dates = pd.to_datetime(self.dates)
    
    def correlate_changepoints(self, changepoint_indices: List[int], window_days: int = 30) -> List[CorrelationResult]:
        """
        Correlate changepoints with nearby geopolitical events.
        
        Parameters:
        -----------
        changepoint_indices : list or array-like
            List of changepoint indices in the time series
        window_days : int, default=30
            Time window (in days) before and after changepoint to search for events
        
        Returns:
        --------
        list of CorrelationResult
        """
        results: List[CorrelationResult] = []
        
        for idx in changepoint_indices:
            if idx >= len(self.dates):
                print(f"Warning: Changepoint index {idx} exceeds date range")
                continue
            
            changepoint_date = self.dates.iloc[idx]
            
            start_date = changepoint_date - timedelta(days=window_days)
            end_date = changepoint_date + timedelta(days=window_days)
            
            mask = (self.events_df['Date'] >= start_date) & (self.events_df['Date'] <= end_date)
            nearby_events = self.events_df[mask].copy()
            
            event_list: List[Dict[str, any]] = []
            for _, event_row in nearby_events.iterrows():
                event_date = event_row['Date']
                days_diff = (event_date - changepoint_date).days
                proximity_score = self.calculate_proximity_score(
                    changepoint_date, event_date, max_days=window_days
                )
                
                event_list.append({
                    'event_date': event_date,
                    'description': event_row['Event'],
                    'category': event_row['Category'],
                    'proximity_score': proximity_score,
                    'days_difference': days_diff
                })
            
            event_list.sort(key=lambda x: x['proximity_score'], reverse=True)
            
            results.append(CorrelationResult(
                changepoint_index=idx,
                changepoint_date=changepoint_date,
                events=event_list
            ))
        
        return results
    
    def calculate_proximity_score(self, changepoint_date: datetime, event_date: datetime, max_days: int = 30) -> float:
        """
        Calculate temporal proximity score between changepoint and event.
        
        The score ranges from 0 to 1, where 1 indicates the event occurred
        on the same day as the changepoint, and 0 indicates the event is
        at the edge of the time window.
        
        Parameters:
        -----------
        changepoint_date : datetime
            Date of the changepoint
        event_date : datetime
            Date of the event
        max_days : int, default=30
            Maximum number of days for the time window
        
        Returns:
        --------
        float : Proximity score between 0 and 1
        """
        days_diff = abs((event_date - changepoint_date).days)
        score = 1 - (days_diff / max_days)
        return max(0.0, score)
    
    def rank_events_by_relevance(self, events: pd.DataFrame, category_weights: Optional[Dict[str, float]] = None) -> pd.DataFrame:
        """
        Rank events by relevance using proximity and category weighting.
        
        Parameters:
        -----------
        events : pd.DataFrame
            DataFrame of events with proximity scores
        category_weights : dict, optional
            Dictionary mapping category names to weight multipliers
            Example: {'War': 1.5, 'Policy': 1.2, 'Economic': 1.0}
        
        Returns:
        --------
        pd.DataFrame : Events ranked by relevance score
        """
        if events.empty:
            return events
        
        events_copy = events.copy()
        
        # Default category weights if not provided
        if category_weights is None:
            category_weights = {
                'War': 1.5,
                'Policy': 1.2,
                'Economic': 1.0,
                'Supply': 1.3,
                'Demand': 1.1
            }
        
        # Calculate relevance score
        events_copy['category_weight'] = events_copy['Category'].map(
            lambda x: category_weights.get(x, 1.0)
        )
        events_copy['relevance_score'] = (
            events_copy['proximity_score'] * events_copy['category_weight']
        )
        
        # Sort by relevance score
        events_copy = events_copy.sort_values('relevance_score', ascending=False)
        
        return events_copy
    
    def generate_correlation_report(self) -> pd.DataFrame:
        """
        Generate a structured correlation report DataFrame.
        
        This method should be called after correlate_changepoints() to
        create a flattened DataFrame suitable for export and analysis.
        
        Returns:
        --------
        pd.DataFrame : Correlation results in tabular format
        """
        # This is a placeholder that will be populated when correlation results exist
        # In practice, this would be called with correlation results as input
        report_data = []
        
        return pd.DataFrame(report_data)


if __name__ == "__main__":
    # Example usage
    from data_loader import EventDataLoader, BrentDataLoader
    
    # Load events
    event_loader = EventDataLoader()
    events_df = event_loader.load_events()
    
    # Load price data to get dates
    price_loader = BrentDataLoader()
    price_df = price_loader.load_data()
    price_df = price_loader.preprocess()
    
    # Create correlator
    correlator = EventCorrelator(events_df, price_df['Date'])
    
    # Example: correlate some changepoint indices
    example_changepoints = [100, 500, 1000]
    results = correlator.correlate_changepoints(example_changepoints, window_days=30)
    
    print("Correlation Results:")
    for result in results:
        print(f"\nChangepoint at index {result.changepoint_index} "
              f"({result.changepoint_date.strftime('%Y-%m-%d')}):")
        if result.events:
            for i, event in enumerate(result.events[:3], 1):  # Show top 3
                print(f"  {i}. {event['description']}")
                print(f"     Date: {event['event_date'].strftime('%Y-%m-%d')}, "
                      f"Proximity: {event['proximity_score']:.2f}, "
                      f"Days diff: {event['days_difference']}")
        else:
            print("  No events found in time window")