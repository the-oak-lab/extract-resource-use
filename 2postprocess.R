setwd("~/extract-resource-use/")

install.packages("DescTools")
install.packages("tidyverse")
install.packages("finalfit")

library("data.table")
library("dplyr")
library("tidyverse")
library("DescTools")
library("tidyverse")
library("finalfit")

gc()

# Get command-line arguments
args <- commandArgs(trailingOnly = TRUE)
file_path <- args[1]

# Print the file path (for debugging purposes)
print(paste("File path:", file_path))

# Load the data
csawesome <- fread(file_path, verbose = TRUE)

csawesome$page_counter <- ifelse(csawesome$page_counter == 0, NA,
                                 csawesome$page_counter)
csawesome$video_counter <- ifelse(csawesome$video_counter == 0, NA,
                                  csawesome$video_counter)
csawesome$act_counter <- ifelse(csawesome$act_counter == 0, NA,
                                csawesome$act_counter)

csawesome$page_time <- ifelse(is.na(csawesome$page_counter), NA,
                              csawesome$time_s_winsorized)
csawesome$video_time <- ifelse(is.na(csawesome$video_counter), NA,
                               csawesome$time_s_winsorized)
csawesome$act_time <- ifelse(is.na(csawesome$act_counter), NA,
                             csawesome$time_s_winsorized)

write.csv(csawesome, file = paste0("postprocess_output.csv"), row.names = FALSE)