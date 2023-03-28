# SQL_SP_To_Git
Get sql code files for all stored procedures in your MSSQL database.

---
# Usage
 - Install and configure the driver to be used by `pyodbc`.
 - Run the script with the following command
 ```
 python automate.py -d=DATABASE_NAME -s=HOST_NAME -u=USER_NAME -p=PASSWORD -t=PORT -r=DRIVER_NAME
 ```
 - Find usage instructions with the following command
 ```
 python automate.py --help
 ```
