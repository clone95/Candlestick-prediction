import os  
from utils import *
import yfinance as yf
import pandas as pd

class Downloader():

    def __init__(self, source_folder, destination_folder, tickers_file):

        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.tickers_file = f'tickers/{tickers_file}.txt'

        with open(self.tickers_file, 'r') as file:
            self.tickers = file.read().split('\n') 



    def download_start_end_tickers(self, start=None, end=None, interval='1d'):
        
        for ticker in self.tickers:
            data = yf.download(
                tickers = (ticker),
                start=start, end=end,
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                # (optional, default is '1d')
                interval = interval,
                auto_adjust = False,
                prepost = True,
                threads = True, )
            dir_name = f'{self.destination_folder}/period/{start}---{end}---{interval}'
            ensure_dir_exists(dir_name)
            data.to_csv(f'{dir_name}/{ticker}.csv')

            self.add_hours(f'{self.destination_folder}/period/{start}---{end}---{interval}')



    def download_interval_tickers(self, interval, period):
        
        for ticker in self.tickers:
            data = yf.download(
                    tickers = (ticker),
                    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                    # (optional, default is '1mo')
                    period = period,
                    # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                    # (optional, default is '1d')
                    interval = interval,
                    auto_adjust = False,
                    prepost = True,
                    threads = True, )
            dir_name = f'{self.destination_folder}/period/{interval}-{period}'
            ensure_dir_exists(dir_name)
            data.to_csv(f'{dir_name}/{ticker}.csv')


    def add_hours(self, dir_name):

        numbs = ['Open', 'Close', 'High', 'Low', 'Adj Close', 'Volume']

        for ticker in os.listdir(dir_name):
            raw_data = pd.read_csv(f'{dir_name}/{ticker}') 

            raw_data['Hour'] = raw_data.groupby('Date').cumcount() + 1
            raw_data['Hour'] = raw_data['Hour'].apply(lambda x: f'0{x}:00:00' if len(str(x))==1 else f'{x}:00:00')  
            raw_data['Date'] = raw_data['Date'] + ' ' + raw_data['Hour']

            for col in numbs:
                raw_data[col] = raw_data[col].apply(lambda x: round(x, 2))

            raw_data.to_csv(f'{dir_name}/{ticker}')
            

