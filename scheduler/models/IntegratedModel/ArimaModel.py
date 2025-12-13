from pycaret.time_series import *
import matplotlib.pyplot as plt

class ArimaModel:

    def __init__(self):
        self.model = None

    '''
    Function to calculate a given number of days in unix
    '''
    def __getUnix(self, days):
        return days * 86400
    
    '''
    Setup Pycaret framework and determine which model best suits the data
    '''
    def assembleModel(self, df):
        df = df.asfreq(freq='d')
        df.index.freq = 'D'
        df['c'] = df['c'].ffill()
        setup(df, fh=5, session_id=123)
        best = create_model('arima')
        result = best
        self.model = result
    
    '''
    Generate predictions based on the best model
    '''
    def predictModel(self, days):
        self.model = finalize_model(self.model)
        prediction = predict_model(self.model, fh=days)
        return prediction
    
    # Ran into problems with the pycaret installation on this file. Fixed it by running:
    # $ python3.11 -m pip install dask --upgrade
    # $ python3.11 -m pip install dask[dataframe]