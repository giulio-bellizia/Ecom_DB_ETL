# TO DOs:
# password handling
# move calculations into DB, rather than in the transform operation
# use sqlalchemy for better abstraction?
# check a better way to download file from SFTP
# isolate files from input

from getpass import getpass
from mysql.connector import connect, Error, errorcode
import my_data


# specify MySQL server details
connection_config = {
    'host': 'localhost',
    'user': 'Giulio',
    'password': 'Capuozz0123!',
}

# provide the name for the database
db_name = "dgt_database"

# provide table name and description
table_name = "master_stock_list"
table_description = "(" \
                    " `SKU CODE (UNIQUE)` varchar(50) NOT NULL," \
                    " `ITEM CODE` varchar(50)," \
                    " `IMAGE SKU 1` varchar(50),"\
                    " `IMAGE SKU 2`	varchar(50)," \
                    " `IMAGE SKU 3`	varchar(50)," \
                    " `IMAGE SKU 4`	varchar(50)," \
                    " `IMAGE SKU 5`	varchar(50)," \
                    " `IMAGE SOURCE` varchar(50)," \
                    " `IMAGE 1 URL`	varchar(512)," \
                    " `IMAGE 2 URL`	varchar(512)," \
                    " `IMAGE 3 URL`	varchar(512)," \
                    " `IMAGE 4 URL`	varchar(512)," \
                    " `IMAGE 5 URL`	varchar(512)," \
                    " `VIDEO 1 URL`	varchar(512)," \
                    " `STOCK STATUS` varchar(50)," \
                    " `CONSTRUCTION TYPE` varchar(50)," \
                    " `MATERIAL` varchar(50)," \
                    " `SUPPLIER LOCATION` varchar(50)," \
                    " `WHEEL OWNER`	varchar(50) NOT NULL," \
                    " `BRAND` varchar(50)," \
                    " `BRAND LOGO` varchar(512)," \
                    " `WHEEL MODEL` varchar(50)," \
                    " `SIZE` varchar(50)," \
                    " `J WIDTH`	varchar(50)," \
                    " `SIZE DESC` varchar(50)," \
                    " `PCD`	varchar(50)," \
                    " `MIN BOLT (IF BLANK)`	smallint(4)," \
                    " `MAX BOLT (IF BLANK)` smallint(4)," \
                    " `MIN LUG (IF BLANK)` smallint(4)," \
                    " `MAX LUG (IF BLANK)` smallint(4)," \
                    " `ET` varchar(50)," \
                    " `MIN ET` varchar(50)," \
                    " `MAX ET` varchar(50)," \
                    " `CB` decimal(10,2)," \
                    " `COLOUR` varchar(50)," \
                    " `FINISH` varchar(50)," \
                    " `WEIGHT LOAD (KG)` decimal(10,2)," \
                    " `WHEEL WEIGHT (KG)` decimal(10,2)," \
                    " `BOLT SEATING` smallint(4)," \
                    " `STAGGERED CODE` varchar(50)," \
                    " `STAGGERED OPTION` varchar(50)," \
                    " `STAGG UNIQUE SKU LOOKUP` varchar(50)," \
                    " `STAGGERED POSITION` varchar(50)," \
                    " `STAGGERED FRONT FILTER` varchar(50)," \
                    " `QUANTITY (SETS AVAILABLE)` smallint(4)," \
                    " `SHIPPING WEIGHT`	smallint(4)," \
                    " `SHIPPING (DOMESTIC)`	decimal(10,2)," \
                    " `SHIPPING (INTERNATIONAL)` decimal(10,2)," \
                    " `MSRP` decimal(10,2)," \
                    " `PRICE MARK UP` decimal(10,2)," \
                    " `TOTAL UNIQUE PRICE (MSRP + MARGIN)` decimal(10,2)," \
                    " `B STOCK IDENTIFIER` varchar(50)," \
                    " `DISCOUNTED PRICE` decimal(10,2)," \
                    " `SINGLE OR SET FILTER` varchar(50)," \
                    " `IMPORT / DISPLAY FILTER`	varchar(50)," \
                    " `BRAND LOGO_[0]` varchar(512)," \
                    " `BRAND BANNER` varchar(512)," \
                    " `BRAND VIDEO 1` varchar(512)," \
                    " `BRAND VIDEO 2` varchar(512)," \
                    " `WHEEL DESCRIPTION` varchar(512)," \
                    " `SEO KEYWORDS` varchar(512)," \
                    " `GROUP IDENTIFIER` varchar(200)," \
                    " PRIMARY KEY (`SKU CODE (UNIQUE)`,`WHEEL OWNER`)" \
                    ")"

# create database function
def create_database(db,cursor,name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
    except db.err as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# connect to the MySQL server and create database if it doesn't exists
# then create the table if it does not exist
try:
    mydb = connect(**connection_config)
    mycursor = mydb.cursor()
    print("Connected to MySQL Server version ", mydb.get_server_info())

    # create the database if it does not exist
    try:
        mycursor.execute("USE {}".format(db_name))
        print("Database {} exists.".format(db_name))
    except Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(mydb, mycursor, db_name)
            print("Database {} created successfully.".format(db_name))
            mydb.database = db_name
        else:
            print(err)
            exit(1)

    # create the table if it does not exist
    try:
        # mycursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        print("Creating table {}: ".format(table_name), end='')
        sql = "CREATE TABLE " + table_name + " " + table_description
        mycursor.execute(sql)
    except Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if mydb.is_connected():
        # list all databases
        mycursor.execute("SHOW DATABASES")
        for x in mycursor:
            print(x)
        mycursor.close()
        mydb.close()
        print("MySQL connection is closed")