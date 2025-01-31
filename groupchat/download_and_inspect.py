# filename: download_and_inspect.py
import pandas as pd

# Step 1: Download the CSV data
url = "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv"
data = pd.read_csv(url)

# Step 2: Print the fields (columns) in the dataset
print(data.columns.tolist())