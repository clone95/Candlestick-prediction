from Downloader import Downloader
from DataProcessor import DataProcessor
downloader = Downloader(source_folder = 'tickers', destination_folder = 'raw_data', tickers_file='test_tickers')

#downloader.download_interval_tickers('1h', '2mo')
downloader.download_start_end_tickers('2018-06-01', '2019-12-30', '1h')

