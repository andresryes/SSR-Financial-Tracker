import pandas as pd
import json

# Sample JSON data
data = {
    "people": [
        {"name": "Alice", "age": 25, "city": "New York"},
        {"name": "Bob", "age": 30, "city": "San Francisco"},
        {"name": "Charlie", "age": 35, "city": "Los Angeles"}
    ]
}

# Writing JSON data to a file
with open('data.json', 'w') as f:
    json.dump(data, f)

# Reading the JSON file into a DataFrame
df = pd.read_json('data.json')

# Assuming the JSON structure needs flattening
df = pd.json_normalize(data, 'people')

# Add a new column 'age_over_30'
df['age_over_30'] = df['age'] > 30

# Filter the DataFrame
df_filtered = df[df['city'] != 'San Francisco']

# Sort the DataFrame
df_sorted = df_filtered.sort_values(by='age')
print(type(df_sorted))
# Display the results
print(df_sorted)
