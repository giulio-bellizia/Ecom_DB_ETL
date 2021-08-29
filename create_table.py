from getpass import getpass
from mysql.connector import connect, Error

# connect to the SQL server
try:
    mydb = connect(
        host="localhost",  # to be later updated with address of client machine
        user="Giulio",  # input("Enter username: "),
        password="Capuozz0123!",  # getpass("Enter password: "),
        database="wheelsdb",
    )
except Error as e:
    print(e)

# create database WheelsDB if it does not exist
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS master_stock_list")  # to be updated with table name as input

# lists all databases
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)
# create table following format of MASTER STOCK LIST from CVS
