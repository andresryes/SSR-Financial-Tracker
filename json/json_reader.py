import json

# Open the JSON file
with open('listado.json', 'r') as file:
    # Load data from JSON file into Python
    data = json.load(file)

    print(type(data))
    # Access the 'students' list and print names and grades
    for student in data['students']:
        print(f'Name: {student["name"]}, Grade: {student["grade"]}')
