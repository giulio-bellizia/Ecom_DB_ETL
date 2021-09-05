# this is the main program for the end-to-end ETL routine
from my_data import db_conn_config, ecom_conn_config, wp_conn_config, \
    ecom_remote_path, wp_remote_path, cnopts, db_metadata, master_stock_list
from my_funcs import conn_db_create, ecom_upload
from wp_extrxfrm import wp_extr, wp_xfrm
from sqlalchemy import create_engine, exc, delete, select
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# establish connection to database, create database if it does not exist
try:
    engine_config = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(*db_conn_config.values())
    db_engine = create_engine(engine_config, echo=False, pool_pre_ping=True)
    db_engine = conn_db_create(db_engine, db_conn_config)
except exc.SQLAlchemyError as err:
    print(err)
    exit(1)

# create master stock list if it does not exist
db_metadata.create_all(db_engine)

# Extract latest product list from suppliers
df_extr = wp_extr(wp_conn_config, cnopts, wp_remote_path)
# Transform imported supplier product list to fit master stock list
df_extrxfrm = wp_xfrm(df_extr)

# # Delete values from old supplier list from table
stmt = delete(master_stock_list).where(master_stock_list.c['WHEEL OWNER'] == 'WHEEL PROS')
with db_engine.begin() as conn:
    conn.execute(stmt)

# Load the updated supplier list into the database
df_extrxfrm.to_sql('master_stock_list', con=db_engine, if_exists='append',index=False, chunksize=1024)
print("Database updated")

# export the database stock list in CVS format to be uploaded in woocommerce
stmt = select(master_stock_list)
df_msl = pd.read_sql_query(stmt, db_engine)
ecom_upload(ecom_conn_config, cnopts, ecom_remote_path, df_msl)

