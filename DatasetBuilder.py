import os 
import pandas as pd
from utils import *


class DatasetBuilder:
    
    def __init__(self, labeled_root_dir, tickers_dir, dates_dir, delta_dir, labeled_data_dir, window):
        
        self.window = window
        self.labeled_data_dir = os.path.join(labeled_root_dir, tickers_dir, dates_dir, delta_dir, labeled_data_dir)

        self.labeled_dataframes = []
        self.datasets = []

        for ticker in os.listdir(self.labeled_data_dir):
            dataframe = pd.read_csv(os.path.join(self.labeled_data_dir, ticker))
            self.labeled_dataframes.append((ticker, dataframe))


    def build_univariate_dataset(self, column='Open'):
        
        for ticker, dataframe in self.labeled_dataframes:
            
            examples = []

            for i in range(0, len(dataframe)-self.window-1):
                window_data = dataframe[column].iloc[i:i+self.window]                
                label = dataframe['class'].iloc[i+self.window+1]
                examples.append((window_data, label))

            print(len(examples))
        