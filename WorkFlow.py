from DatasetGenerator import DatasetGenerator
from ImageTransformer import ImageTransformer
import os


generator = DatasetGenerator(   
                                source_folder = 'tickers', 
                                root_raw = 'raw_data',
                                root_processed_pandas = 'processed/processed_data', 
                                root_processed_images = 'processed/image_data',
                                root_datasets = 'datasets',
                                tickers_file = 'test_tickers',
                                # year-month-day
                                start = '2016-06-30',
                                end = '2019-10-03',
                                delta = '1d'    
                            )

#generator.download_start_end_tickers()

#generator.label_raw_data_percentage(abs_bins = 4, perc_bins = 4)

generator.label_raw_data_open_close()

#generator.pandas_to_images(window_size=10)
#
#transformer = ImageTransformer('processed/image_data/period/2016-06-30---2019-10-03---1d---10')
#
#transformer.crop_images()
#
#generator.build_dataset(window_size=10, ratio=(.8, .1, .1), )