# Automating Stored Procedures to SQL Files

# Import Statements
import pyodbc
import functools
import re
import os
import argparse
import sys


## Argument Variables & Credentials
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-d", "--database", help = "SQL Database Name")
parser.add_argument("-s", "--server", help = "SQL Host Address (Default:localhost)")
parser.add_argument("-u", "--user", help = "User (Default:sa)")
parser.add_argument("-p", "--password", help = "Password (Default:sa9)")
parser.add_argument("-t", "--port", help = "SQL Port (Default:1433)")
 
# Default values
database=None
server="localhost"
password="sa9"
user="sa"
port=1433
driver="FreeTDS"
 
# Read arguments from command line
try:
    args = parser.parse_args()
    if args.database:
        database=args.database
    if args.server:
        server=args.server
    if args.user:
        user=args.user
    if args.password:
        password=args.password
    if args.port:
        port=args.port
except:
    sys.exit("Arguments not available")
    
if port == None or password == None or user == None or server == None or database == None:
    sys.exit("All required arguments aren't initialized")


# Connecting to SQL
try:
    myconn.close()
except:
    print("Connection wasn't open.")
    
print("Connecting to database ...")
myconn = pyodbc.connect(
    server=server,
    database=database,
    user=user,
    tds_version='7.4',
    password=password,
    port=port,
    driver=driver
)
myconn.autocommit = True
print("Connected")

def execQueryWithResult(query, conn):
    mycursor = conn.cursor()
    try:
        myrows = mycursor.execute(query).fetchall()
    except:
        return []
    finally:
        mycursor.close()
    return myrows


# Retrieving all Stored_Procedures
storedProcedures = execQueryWithResult('''
    SELECT 
      ROUTINE_SCHEMA,
      ROUTINE_NAME
    FROM INFORMATION_SCHEMA.ROUTINES
    WHERE ROUTINE_TYPE = 'PROCEDURE';
''', myconn)


# Save stored procedure to a file
def saveStoredProcedureToFile(spSchema, spName):
    spLines = execQueryWithResult(f'EXEC sp_helptext N\'{database}.{spSchema}.{spName}\'', myconn)
    spCode = functools.reduce(lambda a, b: a+b, [line[0] for line in spLines])

    create_procedure_re  = re.compile("create procedure", re.IGNORECASE)

    spCode = """SET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO\n"""+create_procedure_re.sub("ALTER PROCEDURE", spCode)+"\nGO"
    spCode = spCode.replace('\r','')
    writeCodeToFile(spName, spCode)


def writeCodeToFile(spName, spCode):
    os.makedirs(database+"_sp", exist_ok=True)
    with open(database+"_sp/"+spName+".sql", "w") as file:
        # Writing data to a file
        file.write(spCode)


for (spSchema, spName) in storedProcedures:
    saveStoredProcedureToFile(spSchema, spName)
