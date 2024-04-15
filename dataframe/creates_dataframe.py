import pandas as pd

# Load the data
df = pd.read_csv('students.csv')

# Increment the age by 1
df['Age'] += 10

# Filter out students with a grade below 'B'
filtered_df = df[df['Grade'] >= 'B']


# Calculate mean of the values in a column
mean_value = df['Age'].mean()
print(mean_value)

# Summary statistics for numerical columns
summary_stats = df.describe()
print(summary_stats)

# Save the results to a new CSV file
filtered_df.to_csv('updated_students.csv', index=False)
