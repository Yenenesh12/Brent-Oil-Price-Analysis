import { useEffect, useState } from 'react';
import { fetchChangepoints, fetchCorrelations, fetchEvents, fetchPrices, fetchStatistics } from './api';
import './App.css';
import DateRangeFilter from './components/DateRangeFilter';
import EventTimeline from './components/EventTimeline';
import PriceChart from './components/PriceChart';
import Statistics from './components/Statistics';
import VolatilityChart from './components/VolatilityChart';

function App() {
  const [prices, setPrices] = useState(null);
  const [changepoints, setChangepoints] = useState([]);
  const [events, setEvents] = useState([]);
  const [correlations, setCorrelations] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dateRange, setDateRange] = useState({ start: null, end: null });

  useEffect(() => {
    loadData();
  }, [dateRange]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [pricesData, changepointsData, eventsData, correlationsData, statsData] = await Promise.all([
        fetchPrices(dateRange.start, dateRange.end),
        fetchChangepoints(),
        fetchEvents(dateRange.start, dateRange.end),
        fetchCorrelations(),
        fetchStatistics()
      ]);

      setPrices(pricesData);
      setChangepoints(changepointsData);
      setEvents(eventsData);
      setCorrelations(correlationsData);
      setStatistics(statsData);
    } catch (err) {
      setError('Failed to load data. Please ensure the backend server is running.');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeChange = (start, end) => {
    setDateRange({ start, end });
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">
          <h2>Loading Dashboard...</h2>
          <p>Please wait while we fetch the data</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={loadData}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Brent Oil Price Analysis Dashboard</h1>
        <p>Bayesian Change Point Detection & Event Correlation</p>
      </header>

      <main className="App-main">
        <DateRangeFilter 
          onDateRangeChange={handleDateRangeChange}
          minDate={statistics?.date_range?.start}
          maxDate={statistics?.date_range?.end}
        />

        <Statistics stats={statistics} />

        <section className="chart-section">
          <h2>Price History with Change Points</h2>
          <PriceChart 
            prices={prices} 
            changepoints={changepoints}
            events={events}
          />
        </section>

        <section className="chart-section">
          <h2>Volatility Analysis</h2>
          <VolatilityChart prices={prices} />
        </section>

        <section className="chart-section">
          <h2>Event Timeline & Correlations</h2>
          <EventTimeline 
            events={events}
            changepoints={changepoints}
            correlations={correlations}
          />
        </section>
      </main>

      <footer className="App-footer">
        <p>© 2026 Birhan Energies | Data-Driven Energy Market Analysis</p>
      </footer>
    </div>
  );
}

export default App;
