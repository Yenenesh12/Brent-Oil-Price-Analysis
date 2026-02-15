import sys
import os
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.event_correlator import EventCorrelator, CorrelationResult


@pytest.fixture
def sample_events_df() -> pd.DataFrame:
    """Create sample events dataframe for testing."""
    return pd.DataFrame({
        'Date': pd.to_datetime(['2020-01-15', '2020-02-10', '2020-03-20']),
        'Event': ['Event A', 'Event B', 'Event C'],
        'Category': ['War', 'Economic', 'Policy']
    })


@pytest.fixture
def sample_dates() -> pd.Series:
    """Create sample date series for testing."""
    return pd.Series(pd.date_range('2020-01-01', periods=100, freq='D'))


def test_event_correlator_initialization(sample_events_df, sample_dates):
    """Test EventCorrelator initialization."""
    correlator = EventCorrelator(sample_events_df, sample_dates)
    assert correlator is not None
    assert len(correlator.events_df) == 3
    assert len(correlator.dates) == 100


def test_correlate_changepoints_basic(sample_events_df, sample_dates):
    """Test basic changepoint correlation."""
    correlator = EventCorrelator(sample_events_df, sample_dates)
    changepoint_indices = [14]  # Jan 15, 2020 (index 14)
    
    results = correlator.correlate_changepoints(changepoint_indices, window_days=5)
    
    assert len(results) == 1
    assert isinstance(results[0], CorrelationResult)
    assert results[0].changepoint_index == 14
    assert len(results[0].events) >= 1  # Should find Event A


def test_correlate_changepoints_no_events(sample_events_df, sample_dates):
    """Test changepoint correlation when no events are nearby."""
    correlator = EventCorrelator(sample_events_df, sample_dates)
    changepoint_indices = [5]  # Jan 6, 2020 - no events nearby
    
    results = correlator.correlate_changepoints(changepoint_indices, window_days=2)
    
    assert len(results) == 1
    assert len(results[0].events) == 0  # No events in window


def test_calculate_proximity_score(sample_events_df, sample_dates):
    """Test proximity score calculation."""
    correlator = EventCorrelator(sample_events_df, sample_dates)
    
    changepoint_date = datetime(2020, 1, 15)
    event_date_same = datetime(2020, 1, 15)
    event_date_near = datetime(2020, 1, 20)
    event_date_far = datetime(2020, 2, 14)
    
    # Same day should give score of 1.0
    score_same = correlator.calculate_proximity_score(changepoint_date, event_date_same, max_days=30)
    assert score_same == 1.0
    
    # 5 days away should give score around 0.83
    score_near = correlator.calculate_proximity_score(changepoint_date, event_date_near, max_days=30)
    assert 0.8 < score_near < 0.9
    
    # 30 days away should give score of 0.0
    score_far = correlator.calculate_proximity_score(changepoint_date, event_date_far, max_days=30)
    assert score_far == 0.0


def test_rank_events_by_relevance(sample_events_df, sample_dates):
    """Test event ranking by relevance."""
    correlator = EventCorrelator(sample_events_df, sample_dates)
    
    # Add proximity scores to events
    events_with_scores = sample_events_df.copy()
    events_with_scores['proximity_score'] = [0.9, 0.7, 0.5]
    
    category_weights = {'War': 1.5, 'Economic': 1.0, 'Policy': 1.2}
    ranked = correlator.rank_events_by_relevance(events_with_scores, category_weights)
    
    assert 'relevance_score' in ranked.columns
    assert ranked.iloc[0]['Event'] == 'Event A'  # War with high proximity should rank first


def test_correlate_changepoints_multiple(sample_events_df, sample_dates):
    """Test correlation with multiple changepoints."""
    correlator = EventCorrelator(sample_events_df, sample_dates)
    changepoint_indices = [14, 40, 79]  # Multiple changepoints
    
    results = correlator.correlate_changepoints(changepoint_indices, window_days=10)
    
    assert len(results) == 3
    assert all(isinstance(r, CorrelationResult) for r in results)


def test_correlate_changepoints_invalid_index(sample_events_df, sample_dates):
    """Test handling of invalid changepoint index."""
    correlator = EventCorrelator(sample_events_df, sample_dates)
    changepoint_indices = [200]  # Index beyond date range
    
    results = correlator.correlate_changepoints(changepoint_indices, window_days=10)
    
    # Should handle gracefully and return empty or skip invalid indices
    assert len(results) == 0 or all(r.changepoint_index != 200 for r in results)
