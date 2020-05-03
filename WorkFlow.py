from DatasetGenerator import DatasetGenerator

generator = DatasetGenerator(   
                                source_folder = 'tickers', 
                                root_raw_folder = 'raw_data',
                                dataset_folder = 'datasets', 
                                tickers_file='test_tickers',
                                start = '2018-06-05',
                                end = '2019-12-30',
                                delta = '1h'    
                            )

#generator.download_start_end_tickers()

generator.label_raw_data(window_size = 9, n_bins = 4)

