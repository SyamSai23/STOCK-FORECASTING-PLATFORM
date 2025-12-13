import { notification } from 'antd';
import moment from 'moment';
import { isMobile } from 'react-device-detect';
import axiosInstance from './axiosInstance';

const baseUrl = process.env.REACT_APP_API_URL;
const persistRoute = `${baseUrl}/persist`;

// Grab ticker for search
export function fetchTickerData(ticker) {
  if (!ticker) {
    throw new Error("Ticker can't be empty");
  }
  return axiosInstance
    .post('/search', {
      ticker: ticker.toUpperCase(),
    })
    .catch(() => {
      notification.open({
        description: `${ticker.toUpperCase()} : Ticker Doesn't Exit`,
        placement: isMobile ? 'bottomRight' : 'topRight',
        type: 'error',
      });
    });
}

// Fetch Dashboard Data
export function fetchDashboardData(portfolios) {
  return axiosInstance.post('/history_persist', {
    action: 'find_dashboard_data',
    query1: { ticker: { $in: portfolios } },
    // query2: { date: moment().utc().format('Y-MM-DD') },
    query2: {},
    query3: {},
  });
}

// Fetch all tickers in User Portfolio
export function fetchTickers(username = '') {
  return axiosInstance.post('/portfolio', {
    action: 'get_tickers',
    username,
  });
}
// Add ticker to portfolio from search
export function addToPortfolio(ticker, username = '') {
  return axiosInstance
    .post('/persist', {
      action: 'upsert',
      query1: { username },
      query2: { ticker: ticker },
      update_values: {
        date_added: moment().utc(true).format('MM/DD/Y'),
      },
    })
    .then(() => {
      notification.open({
        description: `Successfully Added ${ticker} from your Portfolio`,
        placement: isMobile ? 'bottomRight' : 'topRight',
        type: 'success',
      });
    });
}

// Remove ticker from portfolio from search
export function removeFromPortfolio(ticker, username = '') {
  return axiosInstance
    .post('/persist', {
      action: 'delete',
      query1: { username },
      query2: { ticker: ticker },
    })
    .then(() => {
      notification.open({
        description: `Successfully Removed ${ticker} from your Portfolio`,
        placement: isMobile ? 'bottomRight' : 'topRight',
        type: 'success',
      });
    });
}

// Populate history data table (Ticker, Prices, Dates, Generated Predictions)
export function fetchHistoryData(tickers, dateRange) {
  const date = {
    $lte: moment.utc(dateRange.endDate).format('Y-MM-DD'),
    $gte: moment.utc(dateRange.startDate).format('Y-MM-DD'),
  };
  return axiosInstance.post('/history_persist', {
    action: 'findall',
    query1: { ticker: { $in: tickers } },
    query2: {
      date,
    },
    query3: {},
  });
}

export const UpdateTicker = async (action, collection, query, trimmedTicker, data) => {
  const url = persistRoute;

  // Get update date
  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth() + 1; // getMonth() returns 0-11
    const day = date.getDate();

    // Pad single digit month and day with a zero
    const formattedMonth = month < 10 ? `0${month}` : month;
    const formattedDay = day < 10 ? `0${day}` : day;

    return `${formattedMonth}/${formattedDay}/${year}`;
  };

  const currentDate = new Date();
  const formattedDate = formatDate(currentDate);

  const ticker_data = {
    symbol: trimmedTicker,
    date: formattedDate,
  };

  const addTicker = (currentData, newTicker) => {
    // Check if the ticker already exists
    const exists = currentData.ticker.some((ticker) => ticker.symbol === newTicker.symbol);

    if (exists) {
      throw new Error(`Ticker with symbol ${newTicker.symbol} already exists.`);
    }

    // Ensuring currentData has a ticker array
    const currentTickers = currentData && currentData.ticker ? currentData.ticker : [];

    // Creating a new array of tickers with the new ticker added
    const updatedTickers = [...currentTickers, newTicker];

    // Returning the new object with the updated tickers array
    return {
      ticker: updatedTickers,
    };
  };

  let update_values;

  try {
    update_values = addTicker(data, ticker_data);
    // Update state or perform further actions with updatedData
  } catch (error) {
    console.error(error.message);
    // Handle the error, e.g., show an error message to the user
    // Return an object indicating failure and the error message
    return { success: false, error: error.message };
  }

  const requestData = {
    action: action, // 'add', 'update', or 'remove'
    collection: collection,
    query: query,
    update_values: update_values,
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();
    return { success: true, responseData: responseData };
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
};

export const DeleteTicker = async (action, collection, query, trimmedTicker, data) => {
  const url = persistRoute;

  const removeTicker = (currentData, tickerSymbolToRemove) => {
    // Check if currentData has a ticker array and filter out the specified ticker
    const updatedTickers =
      currentData && currentData.ticker
        ? currentData.ticker.filter((ticker) => ticker.symbol !== tickerSymbolToRemove)
        : [];

    // Returning the new object with the updated tickers array
    return {
      ticker: updatedTickers,
    };
  };

  let update_values = removeTicker(data, trimmedTicker);

  const requestData = {
    action: action, // 'add', 'update', or 'remove'
    collection: collection,
    query: query,
    update_values: update_values,
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();
    return responseData;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
};

export const insertData = async (collectionName, document) => {
  const apiUrl = persistRoute; // Replace with your actual API URL
  const requestData = {
    action: 'insert',
    collection: collectionName,
    document: document,
  };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const jsonResponse = await response.json();
    return jsonResponse; // This is response data in JSON format
  } catch (error) {
    console.error('Error during API call:', error);
  }
};

export function fetchClosingPrice(date, ticker) {
  return axiosInstance.post('/closingPrice', {
    date: date,
    ticker: ticker
  });
}