"""
Flask Backend API for Brent Oil Price Dashboard
Provides REST endpoints for price data, changepoints, and event correlations
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Data paths
DATA_DIR = '../../outputs/data'
PRICES_PATH = os.path.join(DATA_DIR, 'processed_prices.csv')
CHANGEPOINTS_PATH = os.path.join(DATA_DIR, 'changepoint_results.csv')
EVENTS_PATH = os.path.join(DATA_DIR, 'event_correlations.csv')
GEO_EVENTS_PATH = '../../data/events/geopolitical_events.csv'

# Cache for data
_cache = {}

def load_data():
    """Load all data files into cache"""
    if not _cache:
        try:
            _cache['prices'] = pd.read_csv(PRICES_PATH)
            _cache['prices']['Date'] = pd.to_datetime(_cache['prices']['Date'])
            
            _cache['changepoints'] = pd.read_csv(CHANGEPOINTS_PATH)
            _cache['changepoints']['date'] = pd.to_datetime(_cache['changepoints']['date'])
            _cache['changepoints']['lower_ci'] = pd.to_datetime(_cache['changepoints']['lower_ci'])
            _cache['changepoints']['upper_ci'] = pd.to_datetime(_cache['changepoints']['upper_ci'])
            
            _cache['correlations'] = pd.read_csv(EVENTS_PATH)
            _cache['correlations']['changepoint_date'] = pd.to_datetime(_cache['correlations']['changepoint_date'])
            _cache['correlations']['event_date'] = pd.to_datetime(_cache['correlations']['event_date'])
            
            _cache['geo_events'] = pd.read_csv(GEO_EVENTS_PATH)
            _cache['geo_events']['Date'] = pd.to_datetime(_cache['geo_events']['Date'])
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    return True

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get historical price data with optional date filtering"""
    if not load_data():
        return jsonify({'error': 'Data not available'}), 500
    
    df = _cache['prices'].copy()
    
    # Optional date filtering
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        df = df[df['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['Date'] <= pd.to_datetime(end_date)]
    
    # Convert to JSON-friendly format
    data = {
        'dates': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'prices': df['Price'].tolist(),
        'returns': df['Returns'].fillna(0).tolist(),
        'log_returns': df['Log_Returns'].fillna(0).tolist()
    }
    
    return jsonify(data)

@app.route('/api/changepoints', methods=['GET'])
def get_changepoints():
    """Get detected change points"""
    if not load_data():
        return jsonify({'error': 'Data not available'}), 500
    
    df = _cache['changepoints'].copy()
    
    changepoints = []
    for _, row in df.iterrows():
        changepoints.append({
            'id': int(row['changepoint_id']),
            'date': row['date'].strftime('%Y-%m-%d'),
            'index': int(row['index']),
            'lower_ci': row['lower_ci'].strftime('%Y-%m-%d'),
            'upper_ci': row['upper_ci'].strftime('%Y-%m-%d')
        })
    
    return jsonify(changepoints)

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all geopolitical events with optional filtering"""
    if not load_data():
        return jsonify({'error': 'Data not available'}), 500
    
    df = _cache['geo_events'].copy()
    
    # Optional filtering
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if category:
        df = df[df['Category'] == category]
    if start_date:
        df = df[df['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['Date'] <= pd.to_datetime(end_date)]
    
    events = []
    for _, row in df.iterrows():
        events.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'event': row['Event'],
            'category': row['Category'],
            'description': row.get('Description', '')
        })
    
    return jsonify(events)

@app.route('/api/correlations', methods=['GET'])
def get_correlations():
    """Get event-changepoint correlations"""
    if not load_data():
        return jsonify({'error': 'Data not available'}), 500
    
    df = _cache['correlations'].copy()
    
    correlations = []
    for _, row in df.iterrows():
        correlations.append({
            'changepoint_date': row['changepoint_date'].strftime('%Y-%m-%d'),
            'event_date': row['event_date'].strftime('%Y-%m-%d'),
            'event_description': row['event_description'],
            'event_category': row['event_category'],
            'days_difference': int(row['days_difference']),
            'proximity_score': float(row['proximity_score'])
        })
    
    return jsonify(correlations)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get summary statistics"""
    if not load_data():
        return jsonify({'error': 'Data not available'}), 500
    
    prices = _cache['prices']
    
    stats = {
        'total_observations': len(prices),
        'date_range': {
            'start': prices['Date'].min().strftime('%Y-%m-%d'),
            'end': prices['Date'].max().strftime('%Y-%m-%d')
        },
        'price_stats': {
            'mean': float(prices['Price'].mean()),
            'median': float(prices['Price'].median()),
            'std': float(prices['Price'].std()),
            'min': float(prices['Price'].min()),
            'max': float(prices['Price'].max())
        },
        'returns_stats': {
            'mean': float(prices['Returns'].mean()),
            'std': float(prices['Returns'].std()),
            'min': float(prices['Returns'].min()),
            'max': float(prices['Returns'].max())
        },
        'changepoints_detected': len(_cache['changepoints']),
        'events_correlated': len(_cache['correlations'])
    }
    
    return jsonify(stats)

@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    """Calculate rolling volatility"""
    if not load_data():
        return jsonify({'error': 'Data not available'}), 500
    
    df = _cache['prices'].copy()
    window = int(request.args.get('window', 30))
    
    df['volatility'] = df['Returns'].rolling(window=window).std() * (252 ** 0.5)
    df = df.dropna()
    
    data = {
        'dates': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'volatility': df['volatility'].tolist()
    }
    
    return jsonify(data)

if __name__ == '__main__':
    print("Starting Flask API server...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, port=5000)
