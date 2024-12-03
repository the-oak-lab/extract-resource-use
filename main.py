# from utils.utils import Counter

# import pandas as pd
# import numpy as np

import argparse
import subprocess

# preprocessing on the file name for the data
parser = argparse.ArgumentParser(description='Process some data')
parser.add_argument('file_path', type=str, help='data file to process')
args = parser.parse_args()
file_path = args.file_path

# call the R file on the data to extract all the info needed
subprocess.run(['Rscript', 'extractResourceUseNew.R', file_path], check=True)

# adjust as necessary with the utils library

# write all the data on a resulting file name