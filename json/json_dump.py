import json

# Define some data to be written to a JSON file
data = [
    {"name": "Alicia", "age": 25, "city": "Guatemala"},
    {"name": "Bob", "age": 30, "city": "New York"},
    {"name": "Carlos", "age": 35, "city": "Los Angeles"}
]

print(json.dumps(data, indent=2))

# Specify the file to write to
filename = 'data.json'

# Open the file in write mode
with open(filename, 'w') as file:
    # Use json.dump() to write the data to the file
    json.dump(data, file)

print(f'Data successfully written to {filename}')
