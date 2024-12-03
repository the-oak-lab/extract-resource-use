# Get command-line arguments
args <- commandArgs(trailingOnly = TRUE)
file_path <- args[1]

# Print the file path (for debugging purposes)
print(paste("File path:", file_path))

csawesome <- fread(file_path, verbose = TRUE)
