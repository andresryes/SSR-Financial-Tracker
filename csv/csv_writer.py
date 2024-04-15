import csv

# Data to be written to the CSV file
data = [
    ['Nombre', 'Edad', 'Departamento'],
    ['Marcos', 30, 'HR'],
    ['Bob', 25, 'IT'],
    ['Carlos', 35, 'Finanzas']
]

# Open the CSV file in write mode
with open('empleados.csv', 'w', newline='') as csvfile:
    # Create a writer object from the CSV file
    writer = csv.writer(csvfile)
    # Write data to the CSV file
    for row in data:
        writer.writerow(row)
