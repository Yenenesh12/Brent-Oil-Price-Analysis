import { useEffect, useState } from 'react';
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { fetchVolatility } from '../api';
import './VolatilityChart.css';

const VolatilityChart = ({ prices }) => {
  const [volatilityData, setVolatilityData] = useState(null);
  const [window, setWindow] = useState(30);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadVolatility();
  }, [window]);

  const loadVolatility = async () => {
    try {
      setLoading(true);
      const data = await fetchVolatility(window);
      
      const chartData = data.dates.map((date, index) => ({
        date,
        volatility: data.volatility[index],
      }));
      
      setVolatilityData(chartData);
    } catch (error) {
      console.error('Error loading volatility:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading volatility data...</div>;
  }

  if (!volatilityData) {
    return <div>No volatility data available</div>;
  }

  return (
    <div className="volatility-chart-container">
      <div className="controls">
        <label>
          Rolling Window:
          <select value={window} onChange={(e) => setWindow(Number(e.target.value))}>
            <option value={7}>7 days</option>
            <option value={30}>30 days</option>
            <option value={90}>90 days</option>
            <option value={180}>180 days</option>
          </select>
        </label>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={volatilityData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            interval={Math.floor(volatilityData.length / 10)}
          />
          <YAxis 
            label={{ value: 'Annualized Volatility', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="volatility" 
            stroke="#d32f2f" 
            strokeWidth={2}
            dot={false}
            name={`${window}-Day Volatility`}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="volatility-info">
        <p>
          <strong>Volatility Analysis:</strong> This chart shows the rolling {window}-day 
          annualized volatility of Brent oil returns. Higher values indicate periods of 
          greater price uncertainty and market turbulence.
        </p>
      </div>
    </div>
  );
};

export default VolatilityChart;
