import sys
import os
import pytest
import pandas as pd
import numpy as np

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.time_series_analysis import TimeSeriesAnalyzer


@pytest.fixture
def sample_price_df() -> pd.DataFrame:
    """Create sample price dataframe for testing."""
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    prices = 50 + np.cumsum(np.random.randn(100) * 2)  # Random walk
    
    return pd.DataFrame({
        'Date': dates,
        'Price': prices
    })


def test_time_series_analyzer_initialization(sample_price_df):
    """Test TimeSeriesAnalyzer initialization."""
    analyzer = TimeSeriesAnalyzer(sample_price_df)
    assert analyzer is not None
    assert 'Price' in analyzer.df.columns
    assert len(analyzer.df) == 100


def test_test_stationarity(sample_price_df):
    """Test stationarity testing (ADF and KPSS)."""
    analyzer = TimeSeriesAnalyzer(sample_price_df)
    results = analyzer.test_stationarity()
    
    assert 'ADF' in results
    assert 'KPSS' in results
    assert 'statistic' in results['ADF']
    assert 'p_value' in results['ADF']
    assert 'interpretation' in results['ADF']
    assert results['ADF']['interpretation'] in ['Stationary', 'Non-stationary']


def test_calculate_moving_averages(sample_price_df):
    """Test moving average calculation."""
    analyzer = TimeSeriesAnalyzer(sample_price_df)
    df_with_ma = analyzer.calculate_moving_averages(windows=[10, 20])
    
    assert 'MA_10' in df_with_ma.columns
    assert 'MA_20' in df_with_ma.columns
    # First 10 values should be NaN for MA_10
    assert df_with_ma['MA_10'].iloc[:9].isna().all()
    # After window, should have values
    assert not df_with_ma['MA_10'].iloc[10:].isna().all()


def test_calculate_volatility(sample_price_df):
    """Test volatility calculation."""
    analyzer = TimeSeriesAnalyzer(sample_price_df)
    df_with_vol = analyzer.calculate_volatility(windows=[10, 20])
    
    assert 'Volatility_10' in df_with_vol.columns
    assert 'Volatility_20' in df_with_vol.columns
    assert 'Returns' in df_with_vol.columns
    # Volatility should be positive
    assert (df_with_vol['Volatility_10'].dropna() >= 0).all()


def test_detect_outliers(sample_price_df):
    """Test outlier detection."""
    analyzer = TimeSeriesAnalyzer(sample_price_df)
    outliers = analyzer.detect_outliers(threshold=3)
    
    assert isinstance(outliers, pd.DataFrame)
    # With random walk, should have few or no outliers at threshold=3
    assert len(outliers) < len(sample_price_df) * 0.1  # Less than 10%


def test_get_descriptive_stats(sample_price_df):
    """Test descriptive statistics."""
    analyzer = TimeSeriesAnalyzer(sample_price_df)
    stats = analyzer.get_descriptive_stats()
    
    assert 'Price Statistics' in stats
    assert 'mean' in stats['Price Statistics'].index
    assert 'std' in stats['Price Statistics'].index
    assert 'min' in stats['Price Statistics'].index
    assert 'max' in stats['Price Statistics'].index


def test_calculate_volatility_creates_returns(sample_price_df):
    """Test that volatility calculation creates Returns column if missing."""
    analyzer = TimeSeriesAnalyzer(sample_price_df)
    assert 'Returns' not in analyzer.df.columns
    
    analyzer.calculate_volatility(windows=[10])
    
    assert 'Returns' in analyzer.df.columns
    # First return should be NaN
    assert pd.isna(analyzer.df['Returns'].iloc[0])
