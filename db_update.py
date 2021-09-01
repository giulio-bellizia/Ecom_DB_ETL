from getpass import getpass
from mysql.connector import connect, Error

connection_config = {
    'user': 'Giulio',
    'password': 'Capuozz0123!',
    'host': 'localhost',
    # 'database': 'Electronics',
}
# connect to the SQL server
try:
    mydb = connect(**connection_config, database="DGT_database")
except Error as e:
    print(e)

# # create database if it does not exist
# mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE IF NOT EXISTS DGT_database") # to be updated with database name as input
#
# # create table WheelsDB if it does not exist
# # mycursor = mydb.cursor(database="DGT_database")
# mycursor = mydb()
# mycursor.execute("CREATE TABLE IF NOT EXISTS master_stock_list")  # to be updated with table name as input
#
# # lists all databases
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#     print(x)
# # create table following format of MASTER STOCK LIST from CVS
