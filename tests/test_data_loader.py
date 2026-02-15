import sys
import os
import pytest
import pandas as pd

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import BrentDataLoader, DataSummary, EventDataLoader

@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "Price": [100.0, 105.0, 102.0]
    })

def test_load_data(tmp_path):
    test_csv = tmp_path / "test.csv"
    test_data = pd.DataFrame({
        "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "Price": [100.0, 105.0, 102.0]
    })
    test_data.to_csv(test_csv, index=False)
    loader = BrentDataLoader(str(test_csv))
    df = loader.load_data()
    assert len(df) == 3
    assert "Price" in df.columns

def test_preprocess(sample_df):
    loader = BrentDataLoader()
    loader.df = sample_df
    df = loader.preprocess()
    assert "Returns" in df.columns
    assert "Log_Returns" in df.columns

def test_get_summary_stats(sample_df):
    loader = BrentDataLoader()
    loader.df = sample_df
    summary: DataSummary = loader.get_summary_stats()
    assert isinstance(summary, DataSummary)
    assert summary.count == 3
    assert summary.mean == 102.33333333333333


def test_data_loader_with_missing_values(tmp_path):
    """Test data loader handles missing values correctly."""
    test_csv = tmp_path / "test_missing.csv"
    test_data = pd.DataFrame({
        "Date": ["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"],
        "Price": [100.0, None, 102.0, 103.0]
    })
    test_data.to_csv(test_csv, index=False)
    
    loader = BrentDataLoader(str(test_csv))
    df = loader.load_data()
    df = loader.preprocess()
    
    # Missing values should be forward-filled
    assert df['Price'].isna().sum() == 0
    assert len(df) == 4


def test_event_data_loader_initialization():
    """Test EventDataLoader initialization."""
    loader = EventDataLoader()
    assert loader is not None
    assert loader.events_path == 'data/events/geopolitical_events.csv'
