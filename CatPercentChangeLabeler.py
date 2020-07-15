from BaseLabeler import BaseLabeler
import os 
import pandas as pd
import sys
from utils import *
import math

class CatPercentChangeLabeler(BaseLabeler):
    
    def __init__(self, raw_root_dir, tickers_dir, dates_dir, delta_dir, num_classes):
        super().__init__(raw_root_dir, tickers_dir, dates_dir, delta_dir)
        self.num_classes = num_classes
        self.labeling_type = f'cat_pctChg_nc{num_classes}'
        self.labeled_dir = os.path.join('labeled', tickers_dir, dates_dir, delta_dir, self.labeling_type)
        ensure_dir_exists(self.labeled_dir)


    def labeling_workflow(self):
        
        # load raw dataframes
        self.load()
        # preprocess the data
        self.process()
        # label the data
        self.label()
        # save in csv format
        self.save_as_csv()
        # save in ts format
        self.save_as_ts()


    def process(self):
        
        for ticker, dataframe in self.raw_dataframes:
            # set date as datetime
            dataframe.Date = pd.to_datetime(dataframe.Date)
            dataframe.set_index('Date', inplace=True)
            self.processed_dataframes.append((ticker, dataframe)) 


    def label(self):

        for ticker, dataframe in self.processed_dataframes:
            ## calculate and assigne % change bins
            dataframe['pct_change'] = dataframe['Close'].pct_change()
            dataframe['class'] = pd.qcut(dataframe['pct_change'], q=self.num_classes, labels=[x for x in range(0, self.num_classes)])
            # dataframe.to_csv(os.path.join(self.labeled_dir, ticker))
            self.labeled_dataframes.append((ticker, dataframe)) 


    