# Required Libraries
import pandas as pd
import os
###############################################################################

# Warning message about application's limitations
warningStatement = "WARNING: This Application Requires that the Index field compared between tables is Unique, duplicate ID's may result in miss match comparing\n"
print(warningStatement.upper())
selectFilePath = input("What is the filepath for the first file:")

# Display filelist to select file for datatable 1
fileList = os.listdir(selectFilePath)
for i, file in enumerate(fileList):
    print(i, file)

# create datatable 1
selectFilebyIndex = int(input("Select File by Index: "))
fileName = str(fileList[selectFilebyIndex])
DF_ONE = pd.read_csv(selectFilePath + "\\" + fileName, dtype=str, low_memory=False)
for i, column in enumerate(DF_ONE.columns):
    print(i, column)

# Set Index in datatable 1
indexDF_ONE = int(input("Select Index by Index: "))
for i, column in enumerate(DF_ONE.columns):
    if i == indexDF_ONE:
        DF_ONE.set_index(DF_ONE[column], inplace=True)

# Show results
print(DF_ONE.head())
print('FileName: ' + fileName)

#############################################################
selectFilePath2 = input("What is the filepath for the first file:")

# Display filelist to select file for datatable 2
fileList2 = os.listdir(selectFilePath2)
for i, file in enumerate(fileList2):
    print(i, file)

# Create datatable 2
selectFilebyIndex2 = int(input("Select File by Index: "))
fileName2 = str(fileList2[selectFilebyIndex2])
DF_TWO = pd.read_csv(selectFilePath + "\\" + fileName2, dtype=str, low_memory=False)
for i, column in enumerate(DF_TWO.columns):
    print(i, column)

# Set Index in datatable 2
indexDF_TWO = int(input("Select Index by Index: "))
for i, column in enumerate(DF_TWO.columns):
    if i == indexDF_TWO:
        DF_TWO.set_index(DF_TWO[column], inplace=True)

# Show results
print(DF_TWO.head())
print('FileName: ' + fileName2)

#############################################################################
# List to hold missing columns
missingColDF_One = []
missingColDF_Two = []

print("###################")
# Find missing columns in datatable 2
for column in DF_ONE:
    try:
        DF_TWO[column]
    except:
        missingColDF_One.append(str(column))

print("###################")
# Find missing columns in datatable 1
for column in DF_TWO:
    try:
        DF_ONE[column]
    except:
        missingColDF_Two.append(str(column))

# Set index in order so comparison is accurate
DF_TWO.sort_index(inplace=True)
DF_ONE.sort_index(inplace=True)


# Check each shared column to find if differences exist
for column in DF_ONE:
    if str(column) in missingColDF_One:
        pass
    else:
        if DF_ONE[column].equals(DF_TWO[column]):
            pass
        else:
            print("#######################################")
            print("Column '" + str(column) + "' is not a match")


####
print("Missing Columns in datatable:: '" + str(fileName2) + "' | ", missingColDF_One)
print("Missing Columns in second datatable:: '" + str(fileName) + "' | ", missingColDF_Two)

