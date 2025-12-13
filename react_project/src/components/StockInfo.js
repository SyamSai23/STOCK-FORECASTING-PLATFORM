import React from 'react';

// Placeholder function for formatting large numbers
const formatLargeNumber = (number) => {
  // Logic to format the number into a more readable format
  return number;
};

const StockInfo = ({ info }) => {
  // Check if info or info.info is null and return early if so
  if (!info || !info.info) {
    return <div></div>;
  }

  // Destructure the properties for ease of access
  const {
    previous_close,
    pe_ratio,
    day_range,
    dividend_yield,
    year_range,
    primary_exchange,
    market_cap,
    average_volume
  } = info.info;

  // Helper function to handle potentially null values
  const displayValue = (value, formatter = (x) => x, suffix = '') => {
    return value !== null && value !== undefined ? `${formatter(value)}${suffix}` : 'N/A';
  };

  return (
    <div className="stock-info-container">
      <div className="stock-info-item">
        <span className="stock-info-label">Previous Close:</span>
        <span>{displayValue(previous_close)}</span>
      </div>
      <div className="stock-info-item">
        <span className="stock-info-label">P/E Ratio:</span>
        <span>{displayValue(pe_ratio, (x) => x.toFixed(2))}</span>
      </div>
      <div className="stock-info-item">
        <span className="stock-info-label">Day Range:</span>
        <span>{displayValue(day_range.low)} - {displayValue(day_range.high)}</span>
      </div>
      <div className="stock-info-item">
        <span className="stock-info-label">Dividend Yield:</span>
        <span>{displayValue(dividend_yield, (x) => (x * 100).toFixed(2), '%')}</span>
      </div>
      <div className="stock-info-item">
        <span className="stock-info-label">Year Range:</span>
        <span>{displayValue(year_range.low)} - {displayValue(year_range.high)}</span>
      </div>
      <div className="stock-info-item">
        <span className="stock-info-label">Primary Exchange:</span>
        <span>{displayValue(primary_exchange)}</span>
      </div>
      <div className="stock-info-item">
        <span className="stock-info-label">Market Cap:</span>
        <span>{displayValue(market_cap, formatLargeNumber, ' USD')}</span>
      </div>
      <div className="stock-info-item">
        <span className="stock-info-label">Average Volume:</span>
        <span>{displayValue(average_volume, formatLargeNumber, ' M')}</span>
      </div>
    </div>
  );
};

export default StockInfo;

