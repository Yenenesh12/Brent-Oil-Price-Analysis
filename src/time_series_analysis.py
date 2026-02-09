"""
Time series analysis module for Brent oil prices.
Includes trend analysis, stationarity testing, and volatility analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from scipy import stats


class TimeSeriesAnalyzer:
    """Analyze time series properties of oil price data."""
    
    def __init__(self, df, price_col='Price', date_col='Date'):
        """
        Initialize analyzer.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with price data
        price_col : str
            Name of price column
        date_col : str
            Name of date column
        """
        self.df = df.copy()
        self.price_col = price_col
        self.date_col = date_col
        
        if date_col in self.df.columns:
            self.df.set_index(date_col, inplace=True)
    
    def test_stationarity(self):
        """
        Perform stationarity tests (ADF and KPSS).
        
        Returns:
        --------
        dict : Test results
        """
        prices = self.df[self.price_col].dropna()
        
        # Augmented Dickey-Fuller test
        adf_result = adfuller(prices, autolag='AIC')
        
        # KPSS test
        kpss_result = kpss(prices, regression='c', nlags='auto')
        
        results = {
            'ADF': {
                'statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'interpretation': 'Stationary' if adf_result[1] < 0.05 else 'Non-stationary'
            },
            'KPSS': {
                'statistic': kpss_result[0],
                'p_value': kpss_result[1],
                'critical_values': kpss_result[3],
                'interpretation': 'Non-stationary' if kpss_result[1] < 0.05 else 'Stationary'
            }
        }
        
        return results
    
    def calculate_moving_averages(self, windows=[30, 90, 365]):
        """
        Calculate moving averages.
        
        Parameters:
        -----------
        windows : list
            List of window sizes for moving averages
        """
        for window in windows:
            col_name = f'MA_{window}'
            self.df[col_name] = self.df[self.price_col].rolling(window=window).mean()
        
        return self.df
    
    def calculate_volatility(self, windows=[30, 90]):
        """
        Calculate rolling volatility (standard deviation).
        
        Parameters:
        -----------
        windows : list
            List of window sizes for volatility calculation
        """
        if 'Returns' not in self.df.columns:
            self.df['Returns'] = self.df[self.price_col].pct_change()
        
        for window in windows:
            col_name = f'Volatility_{window}'
            self.df[col_name] = self.df['Returns'].rolling(window=window).std() * np.sqrt(252)
        
        return self.df
    
    def detect_outliers(self, threshold=3):
        """
        Detect outliers using z-score method.
        
        Parameters:
        -----------
        threshold : float
            Z-score threshold for outlier detection
        """
        if 'Returns' not in self.df.columns:
            self.df['Returns'] = self.df[self.price_col].pct_change()
        
        returns = self.df['Returns'].dropna()
        # Compute z-scores and align them with the returns index to avoid boolean
        # mask length mismatches when selecting from the full dataframe.
        z_scores = np.abs(stats.zscore(returns))
        z_series = pd.Series(z_scores, index=returns.index)
        mask = z_series > threshold
        # Reindex mask to match the full dataframe index; fill missing with False
        mask_full = mask.reindex(self.df.index, fill_value=False)
        outliers = self.df.loc[mask_full]
        
        return outliers
    
    def get_descriptive_stats(self):
        """Get descriptive statistics."""
        stats_dict = {
            'Price Statistics': self.df[self.price_col].describe(),
        }
        
        if 'Returns' in self.df.columns:
            stats_dict['Returns Statistics'] = self.df['Returns'].describe()
        
        return stats_dict
    
    def plot_price_series(self, figsize=(14, 6)):
        """Plot price time series with moving averages."""
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(self.df.index, self.df[self.price_col], label='Price', linewidth=1)
        
        # Plot moving averages if they exist
        ma_cols = [col for col in self.df.columns if col.startswith('MA_')]
        for col in ma_cols:
            ax.plot(self.df.index, self.df[col], label=col, linewidth=1.5, alpha=0.7)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.set_title('Brent Oil Price Time Series')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_volatility(self, figsize=(14, 6)):
        """Plot rolling volatility."""
        vol_cols = [col for col in self.df.columns if col.startswith('Volatility_')]
        
        if not vol_cols:
            print("No volatility columns found. Run calculate_volatility() first.")
            return None
        
        fig, ax = plt.subplots(figsize=figsize)
        
        for col in vol_cols:
            ax.plot(self.df.index, self.df[col], label=col, linewidth=1.5)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Annualized Volatility')
        ax.set_title('Rolling Volatility of Brent Oil Prices')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_acf_pacf(self, lags=40, figsize=(14, 8)):
        """Plot ACF and PACF."""
        if 'Returns' not in self.df.columns:
            self.df['Returns'] = self.df[self.price_col].pct_change()
        
        returns = self.df['Returns'].dropna()
        
        fig, axes = plt.subplots(2, 1, figsize=figsize)
        
        plot_acf(returns, lags=lags, ax=axes[0])
        axes[0].set_title('Autocorrelation Function (ACF)')
        
        plot_pacf(returns, lags=lags, ax=axes[1])
        axes[1].set_title('Partial Autocorrelation Function (PACF)')
        
        plt.tight_layout()
        return fig
