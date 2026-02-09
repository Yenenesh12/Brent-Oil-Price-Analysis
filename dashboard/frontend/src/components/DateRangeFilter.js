import { useState } from 'react';
import './DateRangeFilter.css';

const DateRangeFilter = ({ onDateRangeChange, minDate, maxDate }) => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleApply = () => {
    onDateRangeChange(startDate || null, endDate || null);
  };

  const handleReset = () => {
    setStartDate('');
    setEndDate('');
    onDateRangeChange(null, null);
  };

  return (
    <div className="date-range-filter">
      <h3>Filter by Date Range</h3>
      <div className="filter-controls">
        <div className="date-input-group">
          <label>Start Date:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            min={minDate}
            max={maxDate}
          />
        </div>

        <div className="date-input-group">
          <label>End Date:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            min={minDate}
            max={maxDate}
          />
        </div>

        <div className="button-group">
          <button className="apply-btn" onClick={handleApply}>
            Apply Filter
          </button>
          <button className="reset-btn" onClick={handleReset}>
            Reset
          </button>
        </div>
      </div>
    </div>
  );
};

export default DateRangeFilter;
