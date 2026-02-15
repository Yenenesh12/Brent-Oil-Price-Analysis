import sys
import os
import pytest
import numpy as np

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.changepoint_model import BayesianChangePointModel

@pytest.fixture
def sample_data() -> np.ndarray:
    return np.random.normal(0, 1, 100)

def test_build_model(sample_data):
    model = BayesianChangePointModel(sample_data, n_changepoints=1)
    built_model = model.build_model()
    assert built_model is not None
    assert "tau" in built_model.named_vars

def test_fit(sample_data):
    model = BayesianChangePointModel(sample_data, n_changepoints=1)
    model.build_model()
    trace = model.fit(draws=100, tune=100, chains=1, cores=1)
    assert trace is not None
    assert "tau" in trace.posterior

def test_summary(sample_data):
    model = BayesianChangePointModel(sample_data, n_changepoints=1)
    model.build_model()
    model.fit(draws=100, tune=100, chains=1, cores=1)
    summary = model.summary()
    assert "tau[0]" in summary.index or "tau" in summary.index