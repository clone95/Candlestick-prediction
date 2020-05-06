import os  
from utils import *
import yfinance as yf
import pandas as pd

class DatasetGenerator():

    def __init__(self, source_folder, root_raw, root_processed, root_dataset, tickers_file, start, end, delta):

        self.source_folder = source_folder

        self.root_raw = root_raw
        self.root_processed = root_processed 
        self.root_dataset = root_dataset 

        self.tickers_file = f'./tickers/{tickers_file}.txt'
        self.root_processed = root_processed 
        self.start = start
        self.end = end
        self.delta = delta
        
        self.raw_data_folder = f'{self.root_raw}/period/{self.start}---{self.end}---{delta}'
        self.processed_data_folder = f'{self.root_processed}/period/{self.start}---{self.end}---{delta}'
        self.dataset_folder = f'{self.root_dataset}/period/{self.start}---{self.end}---{delta}'

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


    def add_hours(self, raw_data_folder):

        numbs = ['Open', 'Close', 'High', 'Low', 'Adj Close', 'Volume']

        for ticker in os.listdir(raw_data_folder):
            raw_data = pd.read_csv(f'{raw_data_folder}/{ticker}') 

            raw_data['Hour'] = raw_data.groupby('Date').cumcount() + 1
            if self.delta == '1h':
                raw_data['Hour'] = raw_data['Hour'].apply(lambda x: f'0{x}:00:00' if len(str(x))==1 else f'{x}:00:00')  
            else:
                raw_data['Hour'] = raw_data['Hour'].apply(lambda x: f'0{x}:00:00' if len(str(x))==1 else f'00:00:00')  
            raw_data['Date'] = raw_data['Date'] + ' ' + raw_data['Hour']

            for col in numbs:
                raw_data[col] = raw_data[col].apply(lambda x: round(x, 2))

            raw_data.to_csv(f'{raw_data_folder}/{ticker}')
            

    def label_raw_data(self, abs_bins, perc_bins):
        
        raw_dataframes = os.listdir(self.raw_data_folder)

        if not len(raw_dataframes) == len(self.tickers):
            raise 'Not all tickers data present in the raw folder'
        ensure_dir_exists(self.processed_data_folder)
        date_col_name = 'Datetime' if self.delta[-1] == 'm' else 'Date'

        for ticker in raw_dataframes:
            # read data and set Date as index
            ticker_data = pd.read_csv(f'{self.raw_data_folder}/{ticker}', parse_dates=True)
            ticker_data[date_col_name] = pd.to_datetime(ticker_data[date_col_name])
            ticker_data.set_index(date_col_name, inplace=True)
            # calculate and assign absolute variation bins
            close_price = ticker_data['Close'].values
            ticker_data['abs_bins'] = pd.qcut(close_price, q=abs_bins, labels=[x for x in range(0, abs_bins)])
            # calculate and assigne % change bins
            ticker_data['pct_change'] = ticker_data['Close'].pct_change()
            ticker_data['pct_change_bins'] = pd.qcut(ticker_data['pct_change'], q=perc_bins, labels=[x for x in range(0, perc_bins)])
            ticker_data.to_csv(f'{self.processed_data_folder}/{ticker}')


    def build_dataset(self, window_size):

        ensure_dir_exists(self.dataset_folder)
        processed_dataframes = os.listdir(self.processed_data_folder)

        for ticker in processed_dataframes:
            ticker_name = ticker.split('.')[0]
            ticker_data = pd.read_csv(f'{self.processed_data_folder}/{ticker}', parse_dates=True)
            # remove last rows 
            rows_to_cut = len(ticker_data) % window_size
            ticker_data = ticker_data[:-rows_to_cut]
            ensure_dir_exists(f'{self.dataset_folder}/{ticker_name}')
            
                        

        
        
