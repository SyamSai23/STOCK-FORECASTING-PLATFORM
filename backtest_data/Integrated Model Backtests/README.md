# Backtest Results on Integrated Model (GPT + Numerical)

This README presents the backtest results of an integrated model combining GPT (Generative Pre-trained Transformer) with numerical analysis. The tests were conducted for small, mid, and large-cap stocks, as well as across different industries.

## Small, Mid, and Large Cap Stocks

- The test encompassed 25 stocks for predictions one day ahead.
- In cases of model disagreement, a "hold" recommendation was returned, enhancing the model's conservative approach and improving recommendation accuracy.
- Overall accuracy:
  - Bullish recommendations: 72%
  - Bearish recommendations: 63%
- Limited instances of 0% accuracy for individual stock recommendations did not significantly affect the overall model accuracy.
- A smaller number of non-hold recommendations may be attributed to certain stocks' limited media or digital footprint.

### Average Accuracy by Market Cap

- **Small Cap:**
  - Bullish: 72%
  - Bearish: 67%
- **Mid Cap:**
  - Bullish: 59%
  - Bearish: 68.57%
- **Large Cap:**
  - Bullish: 69%
  - Bearish: 66.7%
- Small Cap and Large Cap stocks observed the highest number of non-hold recommendations.

## Across Different Industries

- **Tech (AAPL, NVDA, MSFT, GOOGL, AMZN):**
  - Bullish: 68%
  - Bearish: 63%
- **Industrials (BA, CAT, MMM, GE, HON):**
  - Bullish: 69%
  - Bearish: 67%
- **Healthcare (JNJ, PFE, MRK, UNH, AMGN):**
  - Bullish: 69%
  - Bearish: 70%
- **Consumers (DIS, NKE, SBUX, TESLA, HD):**
  - Bullish: 66%
  - Bearish: 83%
- **ESG (NEE, CRM, ACN, ADBE, CSCO):**
  - Bullish: 68%
  - Bearish: 67%
- **Financials (JPM, BAC, V, MA, GS):**
  - Bullish: 72%
  - Bearish: 55%
- **Energy (XOM, CVX, SLB, COP):**
  - Bullish: 62%
  - Bearish: 82%

These results provide valuable insights into the performance and reliability of the integrated model across various market segments and industries.
