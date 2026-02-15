"""
Bayesian change point detection for Brent oil prices.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import pytensor.tensor as pt


@dataclass
class ChangePointResult:
    """Dataclass for change point results."""
    changepoints: np.ndarray
    means: np.ndarray
    trace: az.InferenceData


class BayesianChangePointModel:
    """Bayesian change point model for detecting multiple regime shifts."""

    def __init__(self, data: np.ndarray, n_changepoints: int = 1):
        """
        Parameters:
        -----------
        data : numpy.ndarray
            Time series data (e.g., log returns)
        n_changepoints : int
            Number of change points to detect
        """
        self.data: np.ndarray = np.array(data)
        self.n: int = len(data)
        self.n_changepoints: int = n_changepoints
        self.model: Optional[pm.Model] = None
        self.trace: Optional[az.InferenceData] = None

    def build_model(self) -> pm.Model:
        """Build the Bayesian change point model."""
        data = self.data
        n = self.n
        n_cp = self.n_changepoints
        
        with pm.Model() as model:
            # Priors for change point locations
            tau = pm.DiscreteUniform(
                "tau",
                lower=0,
                upper=n-1,
                shape=n_cp
            )
            
            # Sort change points to ensure ordering using pytensor
            tau_sorted = pt.sort(tau)
            
            # Priors for segment means
            mu = pm.Normal(
                "mu",
                mu=data.mean(),
                sigma=2 * data.std(),
                shape=n_cp + 1
            )
            
            # Prior for observation noise
            sigma = pm.HalfNormal("sigma", sigma=data.std())
            
            # Assign each observation to a segment
            idx = np.arange(n)
            segment = pm.math.sum(
                [idx >= tau_sorted[i] for i in range(n_cp)],
                axis=0
            )
            
            # Likelihood
            pm.Normal(
                "obs",
                mu=mu[segment],
                sigma=sigma,
                observed=data
            )
        
        self.model = model
        return model

    def fit(self, draws: int = 2000, tune: int = 1000, chains: int = 2, cores: int = 1, random_seed: Optional[int] = None) -> az.InferenceData:
        """
        Fit the model using MCMC sampling.
        
        Parameters:
        -----------
        draws : int
            Number of samples to draw
        tune : int
            Number of tuning steps
        chains : int
            Number of MCMC chains
        cores : int
            Number of CPU cores to use
        random_seed : int
            Random seed for reproducibility
        """
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        with self.model:
            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                cores=cores,
                random_seed=random_seed,
                return_inferencedata=True,
                progressbar=True
            )
        
        return self.trace

    def get_changepoint_summary(self) -> pd.DataFrame:
        """Get summary statistics for the posterior."""
        if self.trace is None:
            raise ValueError("Model not fitted yet.")
        
        return az.summary(self.trace)

    def plot_trace(self, figsize: Tuple[int, int] = (14, 10)) -> plt.Figure:
        """Plot trace diagnostics."""
        if self.trace is None:
            raise ValueError("Model not fitted yet.")
        
        fig = az.plot_trace(
            self.trace,
            var_names=["tau", "mu", "sigma"],
            figsize=figsize
        )
        plt.tight_layout()
        return fig

    def plot_results(self, dates: Optional[np.ndarray] = None, figsize: Tuple[int, int] = (16, 10)) -> plt.Figure:
        """
        Plot the data with detected change points.
        
        Parameters:
        -----------
        dates : array-like
            Date array for x-axis
        figsize : tuple
            Figure size
        """
        if self.trace is None:
            raise ValueError("Model not fitted yet.")
        
        # Extract posterior samples
        tau_samples = self.trace.posterior['tau'].values
        tau_samples = tau_samples.reshape(-1, self.n_changepoints)
        tau_mean = tau_samples.mean(axis=0).astype(int)
        
        mu_samples = self.trace.posterior['mu'].values
        mu_samples = mu_samples.reshape(-1, self.n_changepoints + 1)
        mu_mean = mu_samples.mean(axis=0)
        
        # Create figure
        fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
        
        # Plot 1: Data with change points
        ax = axes[0]
        if dates is not None:
            x = pd.to_datetime(dates)
        else:
            x = np.arange(self.n)
        
        ax.plot(x, self.data, 'k-', alpha=0.5, linewidth=0.5, label='Data')
        
        # Plot change points
        for i, tau_idx in enumerate(tau_mean):
            if dates is not None:
                tau_date = pd.to_datetime(dates[tau_idx])
                ax.axvline(tau_date, color='r', linestyle='--',
                          linewidth=2, alpha=0.7,
                          label=f'Change Point {i+1}' if i == 0 else '')
            else:
                ax.axvline(tau_idx, color='r', linestyle='--',
                          linewidth=2, alpha=0.7)
        
        # Plot segment means
        segments = np.concatenate([[0], np.sort(tau_mean), [self.n-1]])
        for i in range(len(segments)-1):
            start, end = int(segments[i]), int(segments[i+1])
            if dates is not None:
                ax.hlines(mu_mean[i], x[start], x[end],
                         colors='blue', linewidth=2, alpha=0.7)
            else:
                ax.hlines(mu_mean[i], start, end,
                         colors='blue', linewidth=2, alpha=0.7)
        
        ax.set_ylabel('Log Returns')
        ax.set_title('Bayesian Change Point Detection Results')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 2: Change point posterior distributions
        ax = axes[1]
        for i in range(self.n_changepoints):
            ax.hist(tau_samples[:, i], bins=50, alpha=0.6,
                   label=f'Change Point {i+1}')
        
        ax.set_xlabel('Time Index' if dates is None else 'Date')
        ax.set_ylabel('Posterior Density')
        ax.set_title('Change Point Posterior Distributions')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig

    def summary(self) -> pd.DataFrame:
        """Return posterior summary."""
        if self.trace is None:
            raise ValueError("Model not fitted yet.")
        
        return az.summary(self.trace)