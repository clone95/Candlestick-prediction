import os, io
from utils import *
import yfinance as yf
import mplfinance as mpf
import math
import matplotlib.pyplot as plt
import pandas as pd
import split_folders
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from sklearn.model_selection import train_test_split


class DataDownloader():

    def __init__(self, source_folder, root_raw, tickers_file, start, end, delta):

        self.source_folder = source_folder
        self.exceptions = []
        self.root_raw = root_raw
        self.tickers_file = f'./tickers/{tickers_file}.txt'

        self.start = start
        self.end = end
        self.delta = delta
        
        self.raw_data_folder = os.path.join(self.root_raw,tickers_file,self.start + '_'+ self.end,delta)
        ensure_dir_exists(self.raw_data_folder)

        with open(self.tickers_file, 'r') as file:
            self.tickers = file.read().split('\n') 


    def download_data(self):

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
        
        # add hours to datetimes
        self.add_hours()

    
    def add_hours(self):
        
        numbs = ['Open', 'Close', 'High', 'Low', 'Adj Close', 'Volume']

        # add "hour" field if not present
        for ticker in os.listdir(self.raw_data_folder):
            raw_data = pd.read_csv(f'{self.raw_data_folder}/{ticker}') 

            raw_data['Hour'] = raw_data.groupby('Date').cumcount() + 1
            if self.delta == '1h':
                raw_data['Hour'] = raw_data['Hour'].apply(lambda x: f'0{x}:00:00' if len(str(x))==1 else f'{x}:00:00')  
            else:
                raw_data['Hour'] = raw_data['Hour'].apply(lambda x: f'00:00:00')  
            raw_data['Date'] = raw_data['Date'] + ' ' + raw_data['Hour']

            # drop "Hour" columns cause it's already in "Date"
            raw_data = raw_data.drop(['Hour'], axis=1)
            for col in numbs:
                raw_data[col] = raw_data[col].apply(lambda x: round(x, 2))

            raw_data.to_csv(f'{self.raw_data_folder}/{ticker}')