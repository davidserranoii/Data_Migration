# Required Libraries
import pandas as pd
import os
# openpyxl will need to be added as a library
###############################################################################
pd.set_option('display.max_columns', None)



selectFilePath = input("What is the file path for the files you wish to load? ")

# File Path Information Displayed for the User
fileList = os.listdir(selectFilePath)
for file in fileList:
    data_file = selectFilePath + "\\" + str(file)
    # Only accepts .xlsx files
    if file.endswith('.xlsx'):
        excelFile = pd.ExcelFile(data_file)
        sheetNames = excelFile.sheet_names
        communityName = input("What is the linking vale for " + str(file) + "? 's' for skip: ")
        if communityName == 's':
            print(str(file) + " skipped.")
        else:
            os.system('mkdir ' + '"' + selectFilePath + '\\' + str(file[:-5]) + '"')
            for sheet in sheetNames:
                try:
                    df = excelFile.parse(sheet, dtype=str)
                    df.fillna("", inplace=True)
                    df = pd.DataFrame(df, dtype=str)
                    # print(df.head())
                    df.insert(loc=0, column='Linking_Value', value=communityName)
                    df.to_csv((selectFilePath + '\\' + str(file[:-5]) + "\\" + str(sheet) + ".csv"), index=False)
                    print(str(sheet) + " loaded.")
                except Exception as e:
                    print(e)
                    print(str(sheet) + 'failed to load in')
