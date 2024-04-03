# Anthony D'Alessandro 3/12/2024
import os
import csv

csvPath = input("Enter file path for CSV File: ")
path = input("Enter file path for Energy Files: ")

# Open CSV File, read data, and store it into a 2-Dimensional list
with open(csvPath, newline='') as csvFile:
    reader = csv.reader(csvFile)
    data = list(reader)

# Loop through 2-Dimensional data list
for element in data:
    # While the first element in each subsequent list has a length less than nine, add zeroes to the
    # front until it is 9 digits long
    while len(element[0]) < 9:
        element[0] = '0' + element[0]
    # Store all file paths in the provided folder of Energy Files
    paths = (os.path.join(root, filename)
        for root, _, filenames in os.walk(path)
        for filename in filenames)
    # Loop through each file path
    for p in paths:
        # If the 'currentAnalogicFile' exists in the file path, replace it with the element at list
        # index 1 (ECTM Number)
        newname = p.replace(element[1], element[0])
        # Rename file
        if newname != p:
            os.rename(p, newname)

# Lines 28 - 32 are simply used to print file names from directory (unnecessary for whole program)
files = os.listdir(path)
count = 1
for file in files:
    print(str(count) + ": " + file)
    count += 1
