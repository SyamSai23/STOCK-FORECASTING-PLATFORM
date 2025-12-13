from .GetData import GetData
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from .GPTModelSimplified import GPTModelSimplified as GPTModel
from .ArimaModel import ArimaModel
from datetime import datetime, timedelta
import json
import pandas as pd

class IntegratedModel:

    def __init__(self):
        self.arimaOutput = None
        self.gptOutput = None
        self.arimaFrame = None
        self.integratedOutput = None
        self.timePeriod = None
        self.historicalData = None
        self.ticker = None
        self.currentDate = None
        self.detailedPrediction = None

    """
    Returns:
        1: Bullish
        -1: Bearish
        0: Uncertain
    """
    def __modelLogic(self):
        self.gptOutput = self.gptOutput.lower()
        self.gptOutput = self.gptOutput.replace(".", "")
        gptDecisions = {'bearish': -1, 'bullish': 1, 'n/a': 0}
        self.gptOutput = gptDecisions.get(self.gptOutput)
        check = self.arimaOutput * self.gptOutput
        if check > 0:
            # Models agree
            if self.gptOutput == -1:
                return -1
            else:
                return 1
        elif check < 0:
            # Differing opinions and niether suggests HOLD
            """
            Current approach is to run backtests and find accuracy of the arima model and the gpt model individually.
            Then use these accuracies to weight their decisions respectively and round to either 1, 0, or -1.
            """
            return 0
        else:
            # gpt model produces uncertain output // or ARIMA predicts no change
            return 0

    def runModel(self, ticker, timePeriod):
        self.ticker = ticker
        self.timePeriod = timePeriod
        self.currentDate = datetime.now()
        # use this format for date 2020-01-13
        #self.currentDate = yyyy-mm-dd --> use this when populating old data
        dateTo = f"{self.currentDate.year}-{self.currentDate.strftime('%m')}-{self.currentDate.strftime('%d')}"
        dateFrom = self.currentDate - timedelta(days=365 * 3)
        dateFrom = f"{dateFrom.year}-{dateFrom.strftime('%m')}-{dateFrom.strftime('%d')}"
        self.historicalData = GetData().assembleDF(ticker, dateFrom, dateTo)
        d1 = self.currentDate - timedelta(days=1) 
        d2 = d1 - timedelta(days=1)
        ### Build ARIMA model
        arima = ArimaModel()
        arima.assembleModel(self.historicalData)
        arimaPrediction = arima.predictModel(self.timePeriod + 2) # +2 since the data goes up to the beginning of today (12:00am so technically it predicts today as well)
        self.arimaFrame = pd.DataFrame(arimaPrediction)
        print(self.arimaFrame)
        predictedPrice = arimaPrediction.iloc[timePeriod - 1]['y_pred']
        currentPrice = self.historicalData.iloc[-1]['c']
        self.arimaOutput = predictedPrice - currentPrice
        ### Build GPT model
        gptMod = GPTModel()
        self.gptOutput = gptMod.runGPT(self.historicalData, ticker, d1, d2)
        ### Build GPT detailed output
        self.detailedPrediction = gptMod.runGPT_Detailed(self.historicalData, ticker, d1, d2, self.arimaOutput) # still need to incorporate the arima output
        ### Run IntegratedModel
        self.integratedOutput = self.__modelLogic()
        return self.integratedOutput
    
    def __formatArimaData(self):
        self.arimaFrame.index = self.arimaFrame.index.to_timestamp()
        self.arimaFrame = self.arimaFrame.rename(columns = {'y_pred' : 'c'})
        print(self.arimaFrame)
        df = pd.concat([self.historicalData, self.arimaFrame])
        result = {"c" : {}}
        for time, value in df.itertuples():
            result['c'][time.timestamp()] = value
        return json.dumps(result)

    """
    Method to return the JSON formatted output of the integrated model to post on the flask API
    """
    def generateJSON(self):
        currentTime = self.currentDate.time().strftime("%I:%M")
        currDate = self.currentDate.strftime("%Y-%m-%d")
        closePrice = self.historicalData.iloc[-1]['c']
        arimaDate = self.currentDate + timedelta(self.timePeriod)
        arimaDate = arimaDate.strftime("%Y-%m-%d") # This holds the date that pertains to the arima models prediction
        quantitative_output = [{
            arimaDate: self.arimaOutput}, # I changed the date in here to the date that is forecasted. Is this right?
            self.__formatArimaData()
        ]
        result = {
            "closing_price": closePrice,
            "date": currDate,
            "integrated_output": self.integratedOutput,
            "quantitative_output": quantitative_output,
            "ticker": self.ticker,
            "time": currentTime
        }
        if self.gptOutput == 1:
            gptOutput_str = "Bullish"
        elif self.gptOutput == -1:
            gptOutput_str = "Bearish"
        else:
            gptOutput_str = "Hold"
        result['integrated_output'] = {
            "detailed_prediction": self.detailedPrediction,
            "general_prediction":  gptOutput_str
        }
        return result
