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

# Arrange the data by time descending
csawesome <- csawesome %>%
  dplyr::arrange(`Anon Student Id`, Time, .by_group = TRUE) %>%
  dplyr::mutate(next_row_time = dplyr::lead(Time, default = dplyr::first(Time)),
    next_student_id = dplyr::lead(`Anon Student Id`,
                                  default = dplyr::first(`Anon Student Id`)),
    time_diff_s = ifelse(next_student_id == `Anon Student Id`,
                         next_row_time - Time, 0)
  )

# Select the columns to keep
csawesome <- csawesome[, c("Anon Student Id", "Problem Name", "Level (Chapter)",
                           "Level (SubChapter)", "time_diff_s", "Selection",
                           "Action", "Input", "Feedback Classification")]

# Write the data to a CSV file
write.csv(csawesome, file = paste0("preprocess_output.csv"), row.names = FALSE)
