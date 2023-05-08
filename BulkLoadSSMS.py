# Packages needed for the program
import os
import pyodbc
import pandas as pd
import socket

##############################

# Testing File Location
print("C:\\Users\\DavidSerrano\\Desktop\\1_Working\\Y_Y Test\\Test Data")

# System Information
selectFilePath = input("What is the file path for the files you wish to load? ")
DATABASE_NAME = input("What is the Database Name: ")
DRIVER_NAME = "SQL SERVER"
hostName = str(socket.gethostname())
SERVER_NAME = hostName + "\\SQLEXPRESS"

# Connection Request
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER_NAME}}};
    DATABASE={{{DATABASE_NAME}}};
    Trust_Connection=yes; 
   #Use if exists below, remove comment
   #uid=<username>;
   #pwd=<password>;
"""

# Write Variables for Connection Request
cnxn = pyodbc.connect(connection_string)
print(cnxn)
cursor = cnxn.cursor()

# File Path Information Displayed for the User
fileList = os.listdir(selectFilePath)
print("There are " + str(len(fileList)) + " files")


# Function to import CSV to SSMS
def bulk_insert(data_file, table_name):
    # data_file is the complete path of the CSV file.
    sql = f"""
            BULK INSERT {table_name}
            FROM '{data_file}'
            WITH
            (
                FORMAT='CSV',
                FIRSTROW = 2,
                FIELDTERMINATOR = ',',
                ROWTERMINATOR = '\\n'
            )
    """.strip()
    return sql


# File Drop list
fileListDropped = []

# Loop through each file in the folder to perform actions directed by user
for file in fileList:
    data_file = selectFilePath + "\\" + str(file)
    print(data_file)

    print("File Path: " + data_file)

    fileName = file[:-4]
    print("File Name: " + fileName)

    try:
        # Encoding Type cp437 or cp1252, datatype = string, low_memory allows for large files
        try:
            df = pd.read_csv(selectFilePath + "\\" + file, low_memory=False, dtype=str)
            print("Added")
        except Exception as e:
            df = pd.read_csv(selectFilePath + "\\" + file, low_memory=False, encoding='cp437', dtype=str)
        # print(df.dtypes)
        # print(df['Referrer Contact HomePhone'])
        df.to_csv(data_file, index=False)
        allHeadersDF = ""
        for col in df.columns:
            allHeadersDF = (str(allHeadersDF) + "[" + str(col) + "] VARCHAR(max), ")
        allHeadersDF = allHeadersDF[:-2]
        # print("All Headers DF: " + allHeadersDF)

    except Exception as e:
        print(e)
        fileListDropped.append(file)
        continue
    print(df.head())
    print("Dropped Files:", fileListDropped)
    print("File Name:" + str(file))

    lookGood = input("Does this look good? 'Y'").upper()
    if lookGood == "Y":

        # SQL Statement to create Table in Server with the headers needed for a merge
        try:
            cursor.execute("CREATE TABLE [" + fileName + "] (" + allHeadersDF + ");")
            # Save Changes
            cursor.commit()

        # Error occurs, likely table already exists
        except Exception as e:
            print("Error: ", e)
            dropTable = input("(CHECK ERROR) Drop PreExisting Table? 'Y'").upper()

            # Drop Existing Table
            if dropTable == 'Y':
                cursor.execute("Drop TABLE [" + fileName + "]")
                # Save Changes
                cursor.commit()

                # Create Table in Server with the headers needed for a merge
                cursor.execute("CREATE TABLE [" + fileName + "] (" + allHeadersDF + ");")
                # Save Changes
                cursor.commit()

        try:
            # Add data to the table in SQL server
            cursor.execute(bulk_insert(data_file, "[" + fileName + "]"))
            cursor.execute(f"""
            DECLARE @TableName nvarchar(100) = N'{fileName}'
            DECLARE @SchemaName nvarchar(100) = N'dbo'
            DECLARE @val varchar(max)
            SELECT @val = COALESCE(@val + 'UPDATE ' + @SchemaName + '.' + @TableName + ' SET [' + COLUMN_NAME + '] = '''' WHERE [' + COLUMN_NAME + '] IS NULL' + '; ','')
            FROM INFORMATION_SCHEMA.COLUMNS C
            WHERE TABLE_NAME = @TableName AND C.DATA_TYPE like '%CHAR%'
            EXEC (@val);
            """)

            print(data_file + " inserted")
            cursor.commit()

            cursor.execute(f"""
            DECLARE @TableName nvarchar(100) = N'{fileName}'
            DECLARE @SchemaName nvarchar(100) = N'dbo'
            DECLARE @val varchar(max)
            SELECT @val = COALESCE(@val + 'UPDATE ' + @SchemaName + '.' + @TableName + ' SET [' + COLUMN_NAME + '] = '''' WHERE [' + COLUMN_NAME + '] = "NAT"' + '; ','')
            FROM INFORMATION_SCHEMA.COLUMNS C
            WHERE TABLE_NAME = @TableName AND C.DATA_TYPE like '%CHAR%'
            EXEC (@val);
            """)

            print(data_file + " inserted")
            cursor.commit()
        except Exception as e:
            print(e)
            cnxn.rollback()
            print('ERROR: Transaction rollback')
    else:
        # File not imported is added to a list
        fileListDropped.append(fileName)
        pass
# End of For Loop

########################
print("The files not added to the database:")
print(fileListDropped)
