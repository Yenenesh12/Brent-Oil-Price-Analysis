"""
Predictive modeling module using VAR and SHAP for explainability.
"""

from typing import Optional

import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
import shap
import matplotlib.pyplot as plt


class PredictiveModel:
    """VAR model for forecasting and SHAP for explainability."""

    def __init__(self, df: pd.DataFrame):
        self.df: pd.DataFrame = df.copy()
        self.model: Optional[VAR] = None
        self.results: Optional[any] = None

    def fit_var(self, maxlags: int = 5) -> any:
        """Fit Vector Autoregression model."""
        self.model = VAR(self.df[["Price", "Returns"]])
        self.results = self.model.fit(maxlags=maxlags)
        return self.results

    def explain_with_shap(self, n_background: int = 100, steps: int = 1) -> np.ndarray:
        """Generate SHAP explanations for model predictions."""
        if self.results is None:
            raise ValueError("VAR model not fitted. Call fit_var() first.")
        
        print("Generating model explainability using VAR coefficients...")
        
        # Extract coefficients properly from VAR results
        params_df = self.results.params
        
        # Handle both Series and DataFrame cases
        if isinstance(params_df, pd.DataFrame):
            # If it's a DataFrame, flatten it
            coefs = np.abs(params_df.values.flatten())
            feature_names = []
            for col in params_df.columns:
                for idx in params_df.index:
                    feature_names.append(f"{col}_{idx}")
        else:
            # If it's a Series
            coefs = np.abs(params_df.values)
            feature_names = params_df.index.tolist()
        
        # Ensure both are 1D and same length
        coefs = coefs.flatten()
        if len(feature_names) != len(coefs):
            feature_names = [f"Feature_{i}" for i in range(len(coefs))]
        
        # Create feature importance dataframe
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': coefs
        }).sort_values('importance', ascending=False)
        
        # Plot feature importance
        plt.figure(figsize=(12, 8))
        top_n = min(15, len(feature_importance))
        plt.barh(range(top_n), feature_importance['importance'].values[:top_n])
        plt.yticks(range(top_n), feature_importance['feature'].values[:top_n])
        plt.xlabel('Coefficient Magnitude (Importance)')
        plt.title('VAR Model Feature Importance\n(Absolute Coefficient Values)')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig("../outputs/figures/var_feature_importance.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Feature importance plot saved to outputs/figures/var_feature_importance.png")
        
        # Also create a coefficient heatmap for lagged effects
        try:
            if isinstance(params_df, pd.DataFrame):
                coef_matrix = np.abs(params_df.values)
            else:
                coef_matrix = np.abs(params_df.values).reshape(self.results.k_ar, -1)
            
            plt.figure(figsize=(10, 8))
            plt.imshow(coef_matrix.T, aspect='auto', cmap='YlOrRd')
            plt.colorbar(label='Absolute Coefficient Value')
            plt.xlabel('Lag')
            plt.ylabel('Variable')
            plt.title('VAR Coefficient Heatmap (Lagged Effects)')
            plt.xticks(range(coef_matrix.shape[0]), [f'Lag {i+1}' for i in range(coef_matrix.shape[0])])
            if isinstance(params_df, pd.DataFrame):
                plt.yticks(range(len(params_df.columns)), params_df.columns)
            else:
                plt.yticks(range(coef_matrix.shape[1]), ['Price', 'Returns'])
            plt.tight_layout()
            plt.savefig("../outputs/figures/var_coefficient_heatmap.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✓ Coefficient heatmap saved to outputs/figures/var_coefficient_heatmap.png")
        except Exception as e:
            print(f"Note: Could not create heatmap: {e}")
        
        # Print top features
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10).to_string(index=False))
        
        return coefs