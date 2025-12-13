import pandas as pd
import requests
import json

class GetData:

    def __init__(self):
        ### Probably want to store this somewhere more secure
        self.accessKey =  "318cd4d14d0c855507f0d4a03ebd566a"
        self.paginationLimit = 1000

    def assembleDF(self, ticker, dateFrom, dateTo):
        # use this format for date2020-01-13
        url = f"http://api.marketstack.com/v1/eod?access_key={self.accessKey}&symbols={ticker}&date_from={dateFrom}&date_to={dateTo}&limit={self.paginationLimit}"
        r = requests.get(url)
        data = json.loads(r.text)
        data = data.get('data')
        dfData = {}
        for row in data:
            index = row.get('date').split('T')[0]
            dfData[index] = row.get('adj_close')
        df = pd.DataFrame.from_dict(dfData, orient="index", columns=['c'])
        df.index = pd.to_datetime(df.index)
        df = df.asfreq(freq='d')
        df['c'] = df['c'].ffill()
        df.index.freq = 'D'
        return df
    
    '''
    Function to combine multiple dataframes representing consecutive time series data
    '''
    def combineDF(self, frames):
        dfList = []
        for frame in frames:
            df = pd.read_csv(frame)
            dfList.append(df)
        result = pd.concat(dfList)
        return result 