import os 
import pandas as pd
from utils import *
from jinja2 import Template


class DatasetBuilder:
    
    def __init__(self, labeled_root_dir, tickers_dir, dates_dir, delta_dir, labeled_data_dir, window):
        
        self.window = window
        self.labeled_dataframe_name = labeled_data_dir
        self.labeled_data_dir = os.path.join(labeled_root_dir, tickers_dir, dates_dir, delta_dir, labeled_data_dir)
        self.base_save_path = os.path.join('datasets', tickers_dir, dates_dir, delta_dir, labeled_data_dir)
        self.labeled_dataframes = []
        self.datasets = []

        ensure_dir_exists(self.base_save_path)

        for ticker in os.listdir(self.labeled_data_dir):
            dataframe = pd.read_csv(os.path.join(self.labeled_data_dir, ticker))
            self.labeled_dataframes.append((ticker, dataframe))


    def build_univariate_dataset(self, column='Open'):

        missing = 'false'
        timestamps = 'false'
        univariate = 'true'

        for ticker, dataframe in self.labeled_dataframes:
            ticker_name = ticker.split('.')[0]
            ts_file_name = ticker_name + '.ts'
            ts_file_save_path = os.path.join(self.base_save_path, ts_file_name) 
            # get unique classes as strings for template
            unique_classes = [x for x in list(set(dataframe['class']))]
            unique_classes = ' '.join([str(int(x)) for x in unique_classes if pd.notnull(x)])

            dataset_descr = Template(f'@problemName {self.labeled_dataframe_name}\n@timeStamps {timestamps}\n@missing {missing}\n@univariate {univariate}\n@classLabel true {unique_classes}\n@data\n'
                                            ).stream(name='foo').dump(ts_file_save_path)

            examples = []

            for i in range(0, len(dataframe)-self.window-1):
                window_data = dataframe[column].iloc[i:i+self.window]                
                label = dataframe['class'].iloc[i+self.window+1]
                examples.append((window_data, label))
            
            with open(ts_file_save_path, 'a') as ts_file:
                for example in examples:
                    values_as_strings = [str(value) for value in example[0]]
                    example_string = ','.join(values_as_strings)
                    ts_file.write(f'\n{example_string}:{str(int(example[1]))}')

                

        