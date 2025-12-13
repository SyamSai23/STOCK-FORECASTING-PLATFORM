import { fetchClosingPrice } from '../API_logic/API';

const getActualResult = async (ticker, date, prediction, historicalClose) => {
    const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split('T')[0]; // Get tomorrow's date in YYYY-MM-DD format
    if (date === today || date === yesterday) {
        return 'N/A';
    }
    if (prediction === 'n/a') {
        return 'N/A';
    }
    const price = await fetchClosingPrice(date, ticker);
    const actualClosingPrice = price.data['Closing Price'];
    const direction = actualClosingPrice - historicalClose;
    // Fetch the closing price of the provided date
    // You may need to adjust the implementation based on your API or data structure
    // Calculate the stock direction based on the actual closing price and previous closing price
    if (direction > 0) {
        return 'Bullish';
    }
    if (direction < 0) {
        return 'Bearish';
    }
    if (direction === 0) {
        return 'N/A';
    }
};

export default getActualResult;
