import rpy2
from utils.py import Counter

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr, data

# from https://rviews.rstudio.com/2022/05/25/calling-r-from-python-with-rpy2/
utils = importr('utils')
base = importr('base')

utils.install_packages('stats')
utils.install_packages('lme4')

stats = importr('stats')
lme4 = importr('lme4')

# importing / installing packages utilized in R code
utils.install_packages('DescTools')
utils.install_packages('tidyverse')
utils.install_packages('finalfit')

# importing libraries utilized in R code
# library('data.table')
# library("dplyr")
# library("tidyverse")
# library("DescTools")
# library("tidyverse")
# library("finalfit")




