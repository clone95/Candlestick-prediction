from DatasetGenerator import DatasetGenerator
import os


generator = DatasetGenerator(   
                                source_folder = 'tickers', 
                                root_raw = 'raw_data',
                                root_processed = 'processed_data', 
                                root_dataset = 'clean_data',
                                tickers_file='test_tickers',
                                # year-month-day
                                start = '2018-06-30',
                                end = '2019-10-03',
                                delta = '1d'    
                            )

#generator.download_start_end_tickers()

#generator.label_raw_data(abs_bins = 4, perc_bins = 4)

generator.build_dataset(window_size=5)

