import master_stock_list_setup
import suppliers_latest
import database_update
import database_export

# connect to the SQL server and create the WheelsBD database if it does not exists yet
master_stock_list_setup

# connect to the SQL server and access the WheelsDB database and create a table following the structure of the master list
# create_table

# export the database stock list in CVS format to be uploaded in woocommerce
# database_export

# fetch latest data from suppliers
# suppliers_fetch

# update the database with the latest data from suppliers
# database_update


