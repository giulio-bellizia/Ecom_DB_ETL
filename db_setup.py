from getpass import getpass
from mysql.connector import connect, Error, errorcode

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
                    " `SKU CODE (UNIQUE)` varchar(50)," \
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
                    " `WHEEL OWNER`	varchar(50)," \
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
                    " `ET` smallint(4)," \
                    " `MIN ET` smallint(4)," \
                    " `MAX ET` smallint(4)," \
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
                    " `GROUP IDENTIFIER` varchar(50)"\
                    ")"

# TABLES['employees'] = (
#     "CREATE TABLE `employees` ("
#     "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
#     "  `birth_date` date NOT NULL,"
#     "  `first_name` varchar(14) NOT NULL,"
#     "  `last_name` varchar(16) NOT NULL,"
#     "  `gender` enum('M','F') NOT NULL,"
#     "  `hire_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`)"
#     ") ENGINE=InnoDB")

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

    # mycursor = mydb.cursor()
    # sql = "CREATE TABLE IF NOT EXISTS " + table_name + msl_structure
    # print(sql)
    # mycursor.execute(sql)

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