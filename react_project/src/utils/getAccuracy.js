import { fetchClosingPrice } from '../API_logic/API';
const getAccuracy = async (data) => {
    const accuracy = {
        bullish_accuracy: '',
        bearish_accuracy: '',
        total_accuracy: ''
    };
    if (data.results?.length > 0) {
        let counts = await getCounts(data);
        let { bullishCorrect, bullishTotal, bearishCorrect, bearishTotal, totalPredictions } = counts;
        
        const totalCorrect = bullishCorrect + bearishCorrect;
        accuracy.bullish_accuracy = `${bullishCorrect}/${bullishTotal}`;
        accuracy.bearish_accuracy = `${bearishCorrect}/${bearishTotal}`;
        accuracy.total_accuracy = totalPredictions > 0 ? `${((totalCorrect / totalPredictions) * 100).toFixed(2)}%` : 'N/A';
    }
    return accuracy;
};

const getCounts = async (data) => {
    let counts = {
        bullishCorrect: 0,
        bullishTotal: 0,
        bearishCorrect: 0,
        bearishTotal: 0,
        totalPredictions: 0
    };
    const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    for (const result of data.results) {
        let date = result.date;
        let ticker = result.ticker;
        if (date == today || date == yesterday) {
            continue;
        }
        let price = await fetchClosingPrice(date, ticker);
        price = price.data['Closing Price'];
        // Determine the direction of the stock
        let stockDirection = price - result.closing_price;                    
        // Loop through each prediction
        let prediction = result.integrated_output.general_prediction;
        let formattedPrediction = prediction.toLowerCase().replace('.', '');
        // Check if the prediction is Bullish or Bearish
        if (formattedPrediction == 'bullish') {
            counts.bullishTotal++;
            counts.totalPredictions++;
            if (stockDirection > 0) {
                counts.bullishCorrect++;
            }
        } else if (formattedPrediction == 'bearish') {
            counts.bearishTotal++;
            counts.totalPredictions++;
            if (stockDirection < 0) {
                counts.bearishCorrect++;
            }
        }
    }
    return counts;
};

export default getAccuracy;
