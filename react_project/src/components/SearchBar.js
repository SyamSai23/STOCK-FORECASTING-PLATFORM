import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedTicker = query.trim().toUpperCase();
    if (trimmedTicker && trimmedTicker.length <= 5) {
    setErrorMessage(''); // Clear any previous error message
    onSearch(trimmedTicker); 
    }
    else {
        // Handle invalid ticker
        console.error('Invalid Ticker: Must be non-empty and up to 5 characters.');
        setErrorMessage('Invalid Ticker: Must be non-empty and up to 5 characters.');
    }
  };

  return ( 
    <div className='Ticker_Search'>
        <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={handleInputChange}
        placeholder="Search..."
      />
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <button type="submit">Search</button>
    </form>
    </div>
  );
};

export default SearchBar;
