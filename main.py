# main program for the end-to-end ETL routine
# establish connection to database (create it if it does not exist)
# create product table if it does not exist
# extract, transform and load onto the database latest product lists from suppliers
# download latest product list from database and save it in a SFTP repository
from my_data import db_conn_config, ecom_conn_config, wp_conn_config, \
    ecom_remote_path, wp_remote_path, cnopts, db_metadata, master_stock_list, jr_url, wr_url
from my_funcs import conn_db_create, ecom_upload
from wp_extrxfrm import wp_extr, wp_xfrm, wp_update
from jr_extrxfrm import jr_extr, jr_xfrm, jr_update
from wr_extrxfrm import wr_extr, wr_xfrm, wr_update
from sqlalchemy import create_engine, exc, select
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

# run wheel pros update
wp_update(wp_conn_config,cnopts,wp_remote_path,db_engine,master_stock_list,wp_extr,wp_xfrm)
# run japan racing update
jr_update(jr_url,db_engine,master_stock_list,jr_extr,jr_xfrm)
# run japan racing update
wr_update(wr_url,db_engine,master_stock_list,wr_extr,wr_xfrm)

# export the database stock list in CVS format to be uploaded in woocommerce
stmt = select(master_stock_list)
df_msl = pd.read_sql_query(stmt, db_engine)
# df_msl.to_csv('sml_test', index=False) # use this for testing
ecom_upload(ecom_conn_config, cnopts, ecom_remote_path, df_msl) # comment it out when testing

