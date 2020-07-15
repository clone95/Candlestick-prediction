from BaseLabeler import BaseLabeler
import os 
import pandas as pd
import sys
from utils import *
import math

class TrendLabeler(BaseLabeler):
    
    def __init__(self, raw_root_dir, tickers_dir, dates_dir, delta_dir):
        super().__init__(raw_root_dir, tickers_dir, dates_dir, delta_dir)
        self.labeling_type = 'trend'

        
    def process(self):
        ...


    def label(self):
        ...


    