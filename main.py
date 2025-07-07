import argparse
import subprocess
import os

from utils.utils import Counter

import pandas as pd

# preprocessing on the file name for the data
parser = argparse.ArgumentParser(description='Process some data')
parser.add_argument('file_path', type=str, help='data file to process')
args = parser.parse_args()
file_path = args.file_path

# call the R file on the data to preprocess the data
prefix_path = os.path.dirname(file_path)
preprocess_script = os.path.join(prefix_path, '1preprocess.R')
subprocess.run(['Rscript', preprocess_script, file_path], check=True)

# add counters for page, video, and activity to the data
counter = Counter(0)

preprocess_output_path = os.path.join(prefix_path, 'preprocess_output.csv')
df = pd.read_csv(preprocess_output_path)

df.loc[:,'page_counter'] = pd.NA
df.loc[:,'video_counter'] = pd.NA
df.loc[:,'act_counter'] = pd.NA

student_list = list(df['Anon Student Id'].unique())

for student in student_list:
    student_rows = df[df['Anon Student Id'] == student]
    for idx in student_rows.index:
        row = df.loc[idx]
        df.loc[idx] = counter.increment_counter(row, df=df, index=idx)
        
counted_path = os.path.join(prefix_path, 'counted.csv')
df.to_csv(counted_path,index=False)

# call the R file on the data to postprocess the data
postprocess_script = os.path.join(prefix_path, '2postprocess.R')
subprocess.run(['Rscript', postprocess_script, counted_path], check=True)

# write all the data on a resulting file name
postprocess_output_path = os.path.join(prefix_path, 'postprocess_output.csv')
df = pd.read_csv(postprocess_output_path)

print(df)

# resulting file name is: "postprocess_output.csv"