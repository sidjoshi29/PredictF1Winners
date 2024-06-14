import pandas as pd

# Load the dataset
df = pd.read_csv('data/final_data.csv')

# Print the range of qualifying times
min_time = df['qualifying_time'].min()
max_time = df['qualifying_time'].max()

print(f"range - {min_time} to {max_time}")
