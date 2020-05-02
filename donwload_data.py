from Downloader import Downloader

downloader = Downloader(source_folder = 'tickers', destination_folder = 'raw_data')

downloader.download_single_ticker(period='1m', interval='1h')