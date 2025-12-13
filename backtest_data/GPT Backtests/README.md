# GPT Model Backtests and Interpretation Guidelines

This README provides insights into GPT model backtests and offers guidelines for interpretation.

## File Structure

In the provided CSV files:

- **Sentiment:** Indicates model output. '1' signifies an upward trend, while '2' denotes a downward trend.
- **Day -1:** Represents the price on the day preceding the prediction generation (open or close, see file name).
- **Day 0:** Indicates the price on the day of prediction.
- **Days 1 and 2:** Reflect the subsequent days.
- **Change on 1 and Change on 2:** Illustrate the percentage change of the stock in the following days (1 or 2), based on opening or closing prices.
- **Successes on Day __ Columns:** '0' signifies a hit (correct prediction), while '1' indicates a miss. The tests were conducted over the course of a year.

## Percent Accuracy (Generalized) for the Past Year:

- **Close 1:** 64.8%
- **Open 1:** 65.7%

## Accuracy of Negative Predictions:

- **Close 1:** 66%
- **Open 1:** 66%

## Accuracy of Positive Predictions:

- **Close 1:** 63.46%
- **Open 1:** 65.60%

These metrics provide an overview of the model's performance over the past year, aiding in understanding its accuracy in both positive and negative predictions based on opening and closing prices.
