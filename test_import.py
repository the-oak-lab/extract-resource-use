import rpy2

rpy2.__path__
print("rpy2 imported successfully")

import time

start_time = time.time()
print("time imported successfully")

import rpy2.robjects as robjects
end_time = time.time()

print(f"Importing rpy2.robjects took {end_time - start_time:.2f} seconds")