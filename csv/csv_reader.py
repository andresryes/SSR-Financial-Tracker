import csv

# Open the CSV file
with open('listado.csv', newline='') as csvfile:
    # Create a reader object from the CSV file
    reader = csv.reader(csvfile, delimiter=',')
    # Skip the header
    next(reader)
    # Iterate over each row in the CSV file
    for row in reader:
        print(f'ID: {row[0]}, Name: {row[1]}, Score: {row[2]}')
