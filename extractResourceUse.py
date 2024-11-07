from utils import Counter

import rpy2.robjects as robjects, pandas2ri
from rpy2.robjects.packages import importr, data
from rpy2.robjects.vectors import StrVector

import pandas as pd
import numpy as np

import argparse

# from https://rviews.rstudio.com/2022/05/25/calling-r-from-python-with-rpy2/
utils = importr('utils')

# importing / installing packages utilized in R code
packages = ('DescTools', 'tidyverse', 'finalfit')
utils.install_packages(StrVector(packages))

# importing libraries utilized in R code
robjects.r('''
library('data.table')
library("dplyr")
library("tidyverse")
library("DescTools")
library("finalfit")
''')

# --------------------------- 1a. open and format the data
robjects.r('gc()')

parser = argparse.ArgumentParser(description='Process some data')
parser.add_argument('file_path', type=str, help='data file to process')
args = parser.parse_args()
file_path = args.file_path

robjects.r('PREFIX_PATH = "{file_path}"')


# puts csawesome_datashop.txt file into R data table named csawesome
robjects.r('''
csawesome <- fread("{file_path}", verbose=TRUE)
''')

# rearranges the csawesome data table, adds more columns
robjects.r('''
csawesome <- csawesome %>%
  dplyr::arrange(`Anon Student Id`, Time, .by_group=TRUE) %>%
  dplyr::mutate(next_row_time = lead(Time, default = dplyr::first(Time)),
                next_student_id = lead(`Anon Student Id`, default = dplyr::first(`Anon Student Id`)),
                time_diff_s = ifelse(next_student_id == `Anon Student Id`,
                                     next_row_time - Time, 0)
  )

csawesome <- csawesome[, c('Anon Student Id', 'Problem Name', 'Level (Chapter)', 'Level (SubChapter)', 'time_diff_s', 'Selection', 'Action', 'Input', 'Feedback Classification')]
''')
csawesome = robjects.r('csawesome')

# --------------------------- 1b. extract resource use
df = pandas2ri.ri2py(csawesome)

counter = Counter(0)

# initialize new columns and iterate over the student_list to increment the counters
df.loc[:,'page_counter'] = pd.NA
df.loc[:,'video_counter'] = pd.NA
df.loc[:,'act_counter'] = pd.NA

student_list = list(df['Anon Student Id'].unique())

for student in student_list:
  df[df['Anon Student Id'] == student] = df[df['Anon Student Id'] == student].apply(counter.increment_counter,axis=1)

# --------------------------- 2. initialize new columns for time spent on each resource
df['page_counter'] = df['page_counter'].replace(0, pd.NA)
df['video_counter'] = df['video_counter'].replace(0, pd.NA)
df['act_counter'] = df['act_counter'].replace(0, pd.NA)

df['page_time'] = df.apply(lambda row: pd.NA if pd.isna(row['page_counter']) else row['time_s_winsorized'], axis=1)
df['video_time'] = df.apply(lambda row: pd.NA if pd.isna(row['video_counter']) else row['time_s_winsorized'], axis=1)
df['act_time'] = df.apply(lambda row: pd.NA if pd.isna(row['act_counter']) else row['time_s_winsorized'], axis=1)

df.to_csv('~/data/all_students_wcounters.csv', index=False)
