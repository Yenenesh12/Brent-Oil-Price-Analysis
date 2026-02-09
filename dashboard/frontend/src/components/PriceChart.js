import { CartesianGrid, Legend, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import './PriceChart.css';

const PriceChart = ({ prices, changepoints, events }) => {
  if (!prices || !prices.dates) {
    return <div>No price data available</div>;
  }

  // Prepare data for chart
  const chartData = prices.dates.map((date, index) => ({
    date,
    price: prices.prices[index],
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const date = payload[0].payload.date;
      const price = payload[0].value;
      
      // Find events on this date
      const dateEvents = events.filter(e => e.date === date);
      
      return (
        <div className="custom-tooltip">
          <p className="label">{`Date: ${date}`}</p>
          <p className="price">{`Price: $${price.toFixed(2)}`}</p>
          {dateEvents.length > 0 && (
            <div className="events">
              <p className="events-title">Events:</p>
              {dateEvents.map((event, idx) => (
                <p key={idx} className="event-item">• {event.event}</p>
              ))}
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="price-chart-container">
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            interval={Math.floor(chartData.length / 10)}
          />
          <YAxis 
            label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="price" 
            stroke="#1e3c72" 
            strokeWidth={2}
            dot={false}
            name="Brent Oil Price"
          />
          
          {/* Add vertical lines for change points */}
          {changepoints.map((cp, index) => (
            <ReferenceLine
              key={`cp-${index}`}
              x={cp.date}
              stroke="red"
              strokeWidth={2}
              strokeDasharray="5 5"
              label={{ value: `CP ${cp.id}`, position: 'top', fill: 'red' }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      
      <div className="changepoints-legend">
        <h3>Detected Change Points:</h3>
        <ul>
          {changepoints.map((cp) => (
            <li key={cp.id}>
              <strong>Change Point {cp.id}:</strong> {cp.date}
              <span className="ci"> (95% CI: {cp.lower_ci} to {cp.upper_ci})</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default PriceChart;
