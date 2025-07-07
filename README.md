# Project Description
This project processes and analyzes student activity logs from CS educational platforms. It combines **R** for preprocessing/postprocessing with **Python** for custom counter logic, producing structured measures of resource use (pages, videos, activities).

---

## Features

* Parses raw logs (`.txt`) of student interactions
* Computes:
  * Time between events
  * Page, video, and activity counters
* Cleans and winsorizes time data
* Outputs tidy CSVs ready for analysis

---

## Dependencies

**R Packages:**

* `data.table`
* `dplyr`
* `tidyverse`
* `DescTools`
* `finalfit`

**Python Packages:**

* `pandas`
* `numpy`
* `rpy2`

---

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/yourusername/extract-resource-use.git
   cd extract-resource-use
   ```

2. **Install R packages:**

   Start R and run:

   ```bash
   install.packages(c("data.table", "dplyr", "tidyverse", "DescTools", "finalfit"))
   ```

3. **Install Python packages:**

   ```bash
   pip3 install pandas numpy rpy2
   ```

4. **Run `main.py`::**

   ```bash
   python3 main.py ./sample.txt
   ```

   **Outputs:**

   * `preprocess_output.csv` (R preprocessing)
   * `counted.csv` (Python counters)
   * `postprocess_output.csv` (R postprocessing)

---

## Project Structure

```
extract-resource-use/
├── 1preprocess.R              # R script for initial cleaning and time_diff computation
├── 2postprocess.R             # R script for final processing
├── utils/
│   └── utils.py               # Counter class (page/video/activity counters)
├── main.py                    # Driver script (R preprocessing + Python counters + R postprocessing)
├── extractResourceUse.py      # IGNORE: alternative script using rpy2 to embed R calls
├── sample.txt                 # Example input data
└── README.md
```