# Open a file in read mode
file = open('file.txt', 'r')
# Read the contents of the file
content = file.read()
print(content)
# Close the file
file.close()

# Now, open the same file in append mode and write to it
file = open('file.txt', 'a')
# Append text to the file
file.write('\nAdding a new line to the file.')
# Close the file
file.close()
