import { useState } from 'react';
import './EventTimeline.css';

const EventTimeline = ({ events, changepoints, correlations }) => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedChangepoint, setSelectedChangepoint] = useState('all');

  // Get unique categories
  const categories = ['all', ...new Set(events.map(e => e.category))];

  // Filter events
  const filteredEvents = events.filter(event => {
    if (selectedCategory !== 'all' && event.category !== selectedCategory) {
      return false;
    }
    return true;
  });

  // Get correlations for selected changepoint
  const getCorrelationsForChangepoint = (cpDate) => {
    return correlations.filter(c => c.changepoint_date === cpDate);
  };

  return (
    <div className="event-timeline-container">
      <div className="filters">
        <div className="filter-group">
          <label>Filter by Category:</label>
          <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
            {categories.map(cat => (
              <option key={cat} value={cat}>
                {cat === 'all' ? 'All Categories' : cat}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Filter by Change Point:</label>
          <select value={selectedChangepoint} onChange={(e) => setSelectedChangepoint(e.target.value)}>
            <option value="all">All Change Points</option>
            {changepoints.map(cp => (
              <option key={cp.id} value={cp.date}>
                Change Point {cp.id} ({cp.date})
              </option>
            ))}
          </select>
        </div>
      </div>

      {selectedChangepoint !== 'all' ? (
        <div className="correlations-view">
          <h3>Events Correlated with Change Point on {selectedChangepoint}</h3>
          <div className="correlations-list">
            {getCorrelationsForChangepoint(selectedChangepoint).map((corr, index) => (
              <div key={index} className="correlation-item">
                <div className="correlation-header">
                  <span className={`category-badge ${corr.event_category.toLowerCase()}`}>
                    {corr.event_category}
                  </span>
                  <span className="event-date">{corr.event_date}</span>
                  <span className="proximity-score">
                    Proximity: {(corr.proximity_score * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="event-description">{corr.event_description}</p>
                <p className="days-diff">
                  {Math.abs(corr.days_difference)} days {corr.days_difference < 0 ? 'before' : 'after'} change point
                </p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="events-view">
          <h3>All Events ({filteredEvents.length})</h3>
          <div className="events-list">
            {filteredEvents.map((event, index) => (
              <div key={index} className="event-item">
                <div className="event-header">
                  <span className={`category-badge ${event.category.toLowerCase()}`}>
                    {event.category}
                  </span>
                  <span className="event-date">{event.date}</span>
                </div>
                <p className="event-description">{event.event}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="correlation-summary">
        <h3>Correlation Summary</h3>
        <div className="summary-stats">
          <div className="stat-card">
            <div className="stat-value">{changepoints.length}</div>
            <div className="stat-label">Change Points Detected</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{correlations.length}</div>
            <div className="stat-label">Event Correlations</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{events.length}</div>
            <div className="stat-label">Total Events</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">
              {correlations.length > 0 
                ? (correlations.reduce((sum, c) => sum + c.proximity_score, 0) / correlations.length * 100).toFixed(0) + '%'
                : 'N/A'}
            </div>
            <div className="stat-label">Avg Proximity Score</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventTimeline;
