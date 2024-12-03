import argparse
import subprocess

from utils.utils import Counter

import pandas as pd

# preprocessing on the file name for the data
parser = argparse.ArgumentParser(description='Process some data')
parser.add_argument('file_path', type=str, help='data file to process')
args = parser.parse_args()
file_path = args.file_path

# call the R file on the data to preprocess the data
subprocess.run(['Rscript', '1preprocess.R', file_path], check=True)

# add counters for page, video, and activity to the data
counter = Counter(0)

df = pd.read_csv("preprocess_output.csv")

df.loc[:,'page_counter'] = pd.NA
df.loc[:,'video_counter'] = pd.NA
df.loc[:,'act_counter'] = pd.NA

student_list = list(df['Anon Student Id'].unique())

for student in student_list:
  df[df['Anon Student Id'] == student] = df[df['Anon Student Id'] == student].apply(counter.increment_counter,axis=1)

df.to_csv("counted.csv",index=False)

# call the R file on the data to postprocess the data
subprocess.run(['Rscript', '2postprocess.R', "counted.csv"], check=True)

# write all the data on a resulting file name
df = pd.read_csv("postprocess_output.csv")
print(df)

# resulting file name is: "postprocess_output.csv"
