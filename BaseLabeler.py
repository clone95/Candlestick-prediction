import os 
import pandas as pd
from utils import *


class BaseLabeler:
    
    def __init__(self, raw_root_dir, tickers_dir, dates_dir, delta_dir):
        
        self.labeling_type = 'base_labeling'
        self.raw_data_final_folder = os.path.join(raw_root_dir, tickers_dir, dates_dir, delta_dir)
        self.processed_dataframes = []
        self.labeled_dataframes = []
        

    def labeling_workflow(self):
        ...


    def load(self):

        self.raw_dataframes = []

        for ticker in os.listdir(self.raw_data_final_folder):
            dataframe = pd.read_csv(os.path.join(self.raw_data_final_folder, ticker))
            self.raw_dataframes.append((ticker, dataframe))


    def process(self):
        ...

    def label(self):
        ...


    def save_as_csv(self):
        
        ensure_dir_exists(self.labeled_dir)

        if self.labeled_dataframes == []:
            raise 'No labeled DataFrame to save!'

        for ticker, dataframe in self.labeled_dataframes:
            dataframe.to_csv(os.path.join(self.labeled_dir, ticker))


    def save_as_ts(self):
        ...

