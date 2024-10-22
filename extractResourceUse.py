from utils.py import Counter

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr, data
from rpy2.robjects.vectors import StrVector

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
robjects.r('PREFIX_PATH = "~/data"')

robjects.r('''
csawesome <- fread(paste0(PREFIX_PATH, '/csawesome_datashop.txt'), verbose=TRUE)
runestone_summary <- read.csv(paste0(PREFIX_PATH, '/complete_course_summary_all_students_12_18.csv'))
''')

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
print(csawesome)


