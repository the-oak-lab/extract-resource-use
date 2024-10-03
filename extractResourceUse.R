setwd("~/extract-resource-use/")

install.packages("DescTools")
install.packages("tidyverse")
install.packages("finalfit")

library('data.table')
library("dplyr")
library("tidyverse")
library("DescTools")
library("tidyverse")
library("finalfit")


gc()


PREFIX_PATH = '~/data'

# --------------------------- 1a. open and format the data
csawesome <- fread(paste0(PREFIX_PATH,'/csawesome_datashop.txt'), verbose=TRUE)
runestone_summary <- read.csv(paste0(PREFIX_PATH,'/complete_course_summary_all_students_12_18.csv'))

# organize the information into a readable format
csawesome <- csawesome %>%
  dplyr::arrange(`Anon Student Id`,Time,.by_group=TRUE) %>%
  dplyr::mutate(next_row_time=lead(Time, default=dplyr::first(Time)),
                next_student_id = lead(`Anon Student Id`, default=dplyr::first(`Anon Student Id`)),
                time_diff_s = ifelse(next_student_id == `Anon Student Id`,
                                     next_row_time - Time,0)
  )

csawesome <- csawesome[,c('Anon Student Id','Problem Name','Level (Chapter)','Level (SubChapter)', 'time_diff_s','Selection','Action','Input','Feedback Classification')]

