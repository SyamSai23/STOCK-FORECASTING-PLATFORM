import React from 'react';
import { useState } from 'react';
import { UpdateTicker, DeleteTicker } from '../API_logic/API';

const Ticker_Search = ({ data, setData, update_data, set_update_data }) => {
  const [ticker, set_ticker] = useState('');
  const [tickerDelete, set_ticker_Delete] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmitadd = (e) => {
    e.preventDefault();
    const trimmedTicker = ticker.trim().toUpperCase();
    if (trimmedTicker && trimmedTicker.length <= 5) {
      const action = 'update';
      const collection = 'mark';
      const query = { user: 'mark' };

      UpdateTicker(action, collection, query, trimmedTicker, data)
        .then((response) => {
          if (response.success) {
            set_update_data(!update_data);
            set_ticker(''); // Clear the ticker input after submission
            setErrorMessage(''); // Clear any previous error message
          } else {
            // Handle the error by setting the error message
            setErrorMessage(response.error);
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          setErrorMessage('An unexpected error occurred.');
        });
    } else {
      // Handle invalid ticker
      console.error('Invalid Ticker: Must be non-empty and up to 5 characters.');
      setErrorMessage('Invalid Ticker: Must be non-empty and up to 5 characters.');
    }
  };

  const handleSubmitDelete = (e) => {
    e.preventDefault();
    const trimmedTicker = tickerDelete.trim().toUpperCase();
    const action = 'update';
    const collection = 'mark';
    const query = { user: 'mark' };
    DeleteTicker(action, collection, query, trimmedTicker, data) // Using fetchData with action 'add'
      .then((data) => {
        set_update_data(!update_data);
        set_ticker_Delete(''); // Clear the ticker input after submission
      });
  };

  return (
    <div class="row">
      <div className="column">
        <div className="gray-card-container-enlarged">
            <div className='Ticker_Search'>
            <h2>Add Ticker</h2>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <form onSubmit={handleSubmitadd}>
            <input
                type="text"
                required
                value={ticker}
                onChange={(e) => set_ticker(e.target.value)}
            />
            <button>Add</button>
            </form>
        </div>
        </div>
      </div>
      <div className="column">
        <div className="gray-card-container-enlarged">
            <div className='Ticker_Search'>
            <h2>Delete Ticker</h2>
            <form onSubmit={handleSubmitDelete}>
            <input
                type="text"
                required
                value={tickerDelete}
                onChange={(e) => set_ticker_Delete(e.target.value)}
            />
            <button>Delete</button>
            </form>
        </div>
        </div>
      </div>
    </div>
  );
};

export default Ticker_Search;
