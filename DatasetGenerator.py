import os  
from utils import *
import yfinance as yf
import pandas as pd

class DatasetGenerator():

    def __init__(self, source_folder, root_raw_folder, root_processed_folder, tickers_file, start, end, delta):

        self.source_folder = source_folder
        self.root_raw_folder = root_raw_folder
        self.tickers_file = f'tickers/{tickers_file}.txt'
        self.root_processed_folder = root_processed_folder 
        self.start = start
        self.end = end
        self.delta = delta
        self.raw_data_folder = f'{self.root_raw_folder}/period/{self.start}---{self.end}---{delta}'
    
        ensure_dir_exists(self.raw_data_folder)

        with open(self.tickers_file, 'r') as file:
            self.tickers = file.read().split('\n') 


    def download_start_end_tickers(self):

        for ticker in self.tickers:
            data = yf.download(
                tickers = (ticker),
                start=self.start, end=self.end,
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                # (optional, default is '1d')
                interval = self.delta,
                auto_adjust = False,
                prepost = True,
                threads = True, )

            data.to_csv(f'{self.raw_data_folder}/{ticker}.csv')

            self.add_hours(self.raw_data_folder)


    def add_hours(self, raw_data_folder):

        numbs = ['Open', 'Close', 'High', 'Low', 'Adj Close', 'Volume']

        for ticker in os.listdir(raw_data_folder):
            raw_data = pd.read_csv(f'{raw_data_folder}/{ticker}') 

            raw_data['Hour'] = raw_data.groupby('Date').cumcount() + 1
            raw_data['Hour'] = raw_data['Hour'].apply(lambda x: f'0{x}:00:00' if len(str(x))==1 else f'{x}:00:00')  
            raw_data['Date'] = raw_data['Date'] + ' ' + raw_data['Hour']

            for col in numbs:
                raw_data[col] = raw_data[col].apply(lambda x: round(x, 2))

            raw_data.to_csv(f'{raw_data_folder}/{ticker}')
            

    def label_raw_data(self, window_size, n_bins):
        
        raw_dataframes = os.listdir(self.raw_data_folder)

        if not len(raw_dataframes) == len(self.tickers):
            raise 'Not all tickers data present in the raw folder'
        ensure_dir_exists()
        for ticker in raw_dataframes:
            # read data and set Date as index
            ticker_data = pd.read_csv(f'{self.raw_data_folder}/{ticker}', index_col=0, parse_dates=True)
            ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])
            ticker_data.set_index('Date', inplace=True)
            # remove last rows 
            rows_to_cut = len(ticker_data) % window_size
            ticker_data = ticker_data[:-rows_to_cut]
            # calculate and assign bins
            ticker_data.to_csv(f'{ticker}.csv')
            close_prices = ticker_data['Close'].values
            ticker_data['bins'] = pd.qcut(close_prices, q=n_bins, labels= [x for x in range(0, n_bins)])
            ticker_data.to_csv(f'{ticker}')
        
        
