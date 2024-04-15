import pandas as pd
import numpy as np
import random

np.random.seed(0)

categories = ["Food", "Transport", "Utilities", "Rent", "Entertainment", "Salary", "Other"]
descriptions = {
    "Food": ["Groceries", "Restaurant", "Coffee", "Snacks"],
    "Transport": ["Bus fare", "Taxi", "Subway ticket", "Gas"],
    "Utilities": ["Electricity", "Water", "Internet", "Gas bill"],
    "Rent": ["Monthly rent"],
    "Entertainment": ["Movies", "Concerts", "Sports event", "Museum tickets"],
    "Salary": ["Monthly salary", "Bonus", "Freelance"],
    "Other": ["Miscellaneous", "Gifts", "Charity", "Unexpected expense"]
}

data = {
    "Amount": np.random.randint(-100, 500, size=100),
    "Category": [random.choice(categories) for _ in range(100)],
    "Description": [random.choice(descriptions[random.choice(categories)]) for _ in range(100)]
}

df = pd.DataFrame(data)

# Dejar positivo solo los salarios
df['Amount'] = np.where(df['Category'] == 'Salary', abs(df['Amount']), df['Amount'])
df['Amount'] = np.where((df['Category'] != 'Salary') & (df['Amount'] > 0), -df['Amount'], df['Amount'])

# Save to CSV
file_path = 'data/financial_data.csv'
df.to_csv(file_path, index=False)

