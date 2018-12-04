import pyodbc
server = 'krishansqlserver.database.windows.net'
database = 'baseline'
username = 'krkusuk'
password = 'College@2019'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
print ('Reading data from table')
tsql = "SELECT name, grain_in_minutes FROM algorithm;"
with cursor.execute(tsql):
    row = cursor.fetchone()
    while row:
        print (str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()