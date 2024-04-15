import json

# JSON string
person_json = '{"name": "Alicia", "age": 25, "city": "Guatemala"}'

# Parse the JSON string
person = json.loads(person_json)
print(type(person))

# Access data from the resulting Python dictionary
print(person['name'])
print(person['age'])
print(person['city'])