import './Statistics.css';

const Statistics = ({ stats }) => {
  if (!stats) {
    return <div>Loading statistics...</div>;
  }

  return (
    <div className="statistics-container">
      <div className="stats-grid">
        <div className="stat-box">
          <h3>Data Range</h3>
          <p className="stat-main">{stats.date_range.start}</p>
          <p className="stat-sub">to</p>
          <p className="stat-main">{stats.date_range.end}</p>
        </div>

        <div className="stat-box">
          <h3>Total Observations</h3>
          <p className="stat-main">{stats.total_observations.toLocaleString()}</p>
          <p className="stat-sub">daily prices</p>
        </div>

        <div className="stat-box">
          <h3>Average Price</h3>
          <p className="stat-main">${stats.price_stats.mean.toFixed(2)}</p>
          <p className="stat-sub">±${stats.price_stats.std.toFixed(2)} std</p>
        </div>

        <div className="stat-box">
          <h3>Price Range</h3>
          <p className="stat-main">${stats.price_stats.min.toFixed(2)}</p>
          <p className="stat-sub">to</p>
          <p className="stat-main">${stats.price_stats.max.toFixed(2)}</p>
        </div>

        <div className="stat-box">
          <h3>Change Points</h3>
          <p className="stat-main">{stats.changepoints_detected}</p>
          <p className="stat-sub">structural breaks</p>
        </div>

        <div className="stat-box">
          <h3>Event Correlations</h3>
          <p className="stat-main">{stats.events_correlated}</p>
          <p className="stat-sub">identified links</p>
        </div>
      </div>
    </div>
  );
};

export default Statistics;
