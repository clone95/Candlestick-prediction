from DataDownloader import DataDownloader

from BaseLabeler import BaseLabeler
from CatPercentChangeLabeler import CatPercentChangeLabeler
from TrendLabeler import TrendLabeler

from ImageTransformer import ImageTransformer

import os

root_raw = 'raw_data'
source_tickers = 'tickers'
tickers = 'test_tickers'
start = '2018-07-30'
end = '2020-02-02'
delta = '1h'
start_end = start + '_' + end

#generator = DataDownloader (   
#                                source_folder = 'tickers', 
#                                root_raw = root_raw,
#                                tickers_file = test_tickers,
#                                # year-month-day
#                                start = start,
#                                end = end,
#                                delta = delta 
#                            )
#
#generator.download_data()
#base_labeler = BaseLabeler(root_raw, tickers, start_end, delta)
perc_labeler = CatPercentChangeLabeler(root_raw, tickers, start_end, delta, window=10, num_classes=5)
perc_labeler.labeling_workflow()

    #labeler.funcname()
#generator.label_raw_data_percentage(abs_bins = 4, perc_bins = 4)

#generator.label_raw_data_open_close()

#generator.pandas_to_images(window_size=10, class_type='oc')
#
#transformer = ImageTransformer('processed/image_data/2016-06-30---2019-10-03---1d---10---oc')
#
#transformer.crop_images()
#
#generator.build_dataset(window_size=10, ratio=(.8, .1, .1), )