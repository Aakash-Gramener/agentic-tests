# filename: plot_weight_vs_horsepower.py
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset again
url = "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv"
data = pd.read_csv(url)

# Step 3: Create a plot
plt.figure(figsize=(10, 6))
plt.scatter(data['Weight'], data['Horsepower(HP)'], alpha=0.5)
plt.title('Relationship between Weight and Horsepower')
plt.xlabel('Weight')
plt.ylabel('Horsepower (HP)')
plt.grid(True)

# Step 4: Save the plot to a file
plt.savefig('weight_vs_horsepower.png')
plt.close()