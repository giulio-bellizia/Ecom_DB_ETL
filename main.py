from sqlalchemy import create_engine, exc, delete
from my_data import db_conn_config, db_metadata, master_stock_list
from my_funcs import conn_db_create
import pandas as pd
from wp_extrxfrm import wp_extr, wp_xfrm, wp_conn_config, cnopts, wp_remote_path

# establish connection to database, create database if it does not exist
try:
    engine_config = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(*db_conn_config.values())
    db_engine = create_engine(engine_config, echo=False, pool_pre_ping=True)
    db_engine = conn_db_create(db_engine)
except exc.SQLAlchemyError as err:
    print(err)
    exit(1)

# create master stock list if it does not exist
db_metadata.create_all(db_engine)

# # Extract latest product list from suppliers
df_extr = wp_extr(wp_conn_config, cnopts, wp_remote_path)
# # Transform imported supplier product list to fit master stock list
df_extrxfrm = wp_xfrm(df_extr)

# df_extrxfrm.to_csv("wheelInvPriceData.csv", index=False)
# df_extrxfrm = pd.read_csv("wheelInvPriceData.csv")

# # Delete from table values from old supplier list
stmt = delete(master_stock_list).where(master_stock_list.c['WHEEL OWNER'] == 'WHEEL PROS')
with db_engine.begin() as conn:
    conn.execute(stmt)

# Load the updated supplier list into the database
df_extrxfrm.to_sql('master_stock_list', con=db_engine, if_exists='append',index=False, chunksize=1024)

# export the database stock list in CVS format to be uploaded in woocommerce
# database_export

# query = 'select * from master_stock_list'
# results = pd.read_sql_query(query, db_engine)
# results.to_csv("wheelpros_exported1.csv", index=False)




# to insert in chunksize
# DataFrame.to_sql(name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)


# with engine.begin() as connection:
#     r1 = connection.execute(table1.select())
#     connection.execute(table1.insert(), {"col1": 7, "col2": "this is some data"})