from sqlalchemy import create_engine, exc
from my_data import db_conn_config, db_metadata
from my_funcs import conn_db_create
# establish connection to database, create database if it does not exist
try:
    engine_config = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(*db_conn_config.values())
    db_engine = create_engine(engine_config, echo=False, pool_pre_ping=True)
    db_engine = conn_db_create(db_engine)
except exc.SQLAlchemyError as err:
    print(err)
    exit(1)

# create table if it does not exist
db_metadata.create_all(db_engine)

# fetch latest data from suppliers
# suppliers_fetch

# export the database stock list in CVS format to be uploaded in woocommerce
# database_export



# try:
#     # mycursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
#     print("Creating table {}: ".format(table_name), end='')
#     sql = "CREATE TABLE " + table_name + " " + table_description
#     mycursor.execute(sql)
# except Error as err:
#     if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#         print("already exists.")
#     else:
#         print(err.msg)
# else:
#     print("OK")


# to insert in chunksize
# DataFrame.to_sql(name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)


# with engine.begin() as connection:
#     r1 = connection.execute(table1.select())
#     connection.execute(table1.insert(), {"col1": 7, "col2": "this is some data"})