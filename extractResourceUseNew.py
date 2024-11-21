from utils.utils import Counter

import pandas as pd
import numpy as np

import argparse

parser = argparse.ArgumentParser(description='Process some data')
parser.add_argument('file_path', type=str, help='data file to process')
args = parser.parse_args()
file_path = args.file_path


counter = Counter(0)
