from sqlalchemy import MetaData, Table, Column, SmallInteger, String, Float, PrimaryKeyConstraint
import pysftp
import warnings
from dotenv import load_dotenv
import os

load_dotenv('.env')
warnings.filterwarnings('ignore')

# MySQL database details
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_conn_config = {
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'database': db_name
}

# WP SFTP server details
wp_host = os.getenv('WP_HOST')
wp_username = os.getenv('WP_USERNAME')
wp_password = os.getenv('WP_PASSWORD')
wp_remote_path = os.getenv('WP_REMOTE_PATH')
wp_conn_config = {
    'host': wp_host,
    'username': wp_username,
    'password': wp_password,
}

# JR url with api key to get product list
jr_url = os.getenv('JR_URL')

# WR url to get product list
wr_url = os.getenv('WR_URL')

# AP url to get product list
ap_url = os.getenv('AP_URL')

# Portal SFTP server details
ecom_host = os.getenv('ECOM_HOST')
ecom_username = os.getenv('ECOM_USERNAME')
ecom_password = os.getenv('ECOM_PASSWORD')
ecom_remote_path = os.getenv('ECOM_REMOTE_PATH')
ecom_conn_config = {
    'host': ecom_host,
    'username': ecom_username,
    'password': ecom_password,
}

# Disable hot key checking
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Create/set suppliers raw data repository
suppliers_raw_data_dir = os.getenv('SUPPLIERS_DATA_DIR')
directory = 'suppliers_raw_data'
suppliers_path = os.path.join(suppliers_raw_data_dir,directory)

# Suppliers list
wp_name = os.getenv('WP_NAME')
jr_name = os.getenv('JR_NAME')
wr_name = os.getenv('WR_NAME')
ap_name = os.getenv('AP_NAME')
suppliers_list = {
    'WP': wp_name,
    'JR': jr_name,
    'WR': wr_name,
    'AP': ap_name
}

# database metadata
db_metadata = MetaData()
master_stock_list = Table(
    'master_stock_list',
    db_metadata,
    Column('SKU CODE (UNIQUE)', String(50), nullable=False),
    Column('ITEM CODE', String(200)),
    Column('IMAGE SKU 1', String(50)),
    Column('IMAGE SKU 2', String(50)),
    Column('IMAGE SKU 3', String(50)),
    Column('IMAGE SKU 4', String(50)),
    Column('IMAGE SKU 5', String(50)),
    Column('IMAGE SOURCE', String(50)),
    Column('IMAGE 1 URL', String(500)),
    Column('IMAGE 2 URL', String(500)),
    Column('IMAGE 3 URL', String(500)),
    Column('IMAGE 4 URL', String(500)),
    Column('IMAGE 5 URL', String(500)),
    Column('VIDEO 1 URL', String(500)),
    Column('STOCK STATUS', String(50)),
    Column('CONSTRUCTION TYPE', String(50)),
    Column('MATERIAL', String(50)),
    Column('SUPPLIER LOCATION', String(50)),
    Column('WHEEL OWNER', String(50), nullable=False),
    Column('BRAND', String(50)),
    Column('BRAND LOGO', String(500)),
    Column('WHEEL MODEL', String(50)),
    Column('SIZE', String(50)),
    Column('J WIDTH', String(50)),
    Column('SIZE DESC', String(50)),
    Column('PCD', String(500)),
    Column('MIN BOLT (IF BLANK)', SmallInteger),
    Column('MAX BOLT (IF BLANK)', SmallInteger),
    Column('MIN LUG (IF BLANK)', SmallInteger),
    Column('MAX LUG (IF BLANK)', SmallInteger),
    Column('ET', String(500)),
    Column('MIN ET', String(50)),
    Column('MAX ET', String(50)),
    Column('CB', String(500)),
    Column('COLOUR', String(50)),
    Column('FINISH', String(50)),
    Column('WEIGHT LOAD (KG)', Float),
    Column('WHEEL WEIGHT (KG)', Float),
    Column('BOLT SEATING', SmallInteger),
    Column('STAGGERED CODE', String(50)),
    Column('STAGGERED OPTION', String(50)),
    Column('STAGG UNIQUE SKU LOOKUP', String(50)),
    Column('STAGGERED POSITION', String(50)),
    Column('STAGGERED FRONT FILTER', String(50)),
    Column('QUANTITY (SETS AVAILABLE)', SmallInteger),
    Column('SHIPPING WEIGHT', SmallInteger),
    Column('SHIPPING (DOMESTIC)', Float),
    Column('SHIPPING (INTERNATIONAL)', Float),
    Column('MSRP', Float),
    Column('PRICE MARK UP', Float),
    Column('TOTAL UNIQUE PRICE (MSRP + MARGIN)', Float),
    Column('B STOCK IDENTIFIER', String(50)),
    Column('DISCOUNTED PRICE', Float),
    Column('SINGLE OR SET FILTER', String(50)),
    Column('IMPORT / DISPLAY FILTER', String(50)),
    Column('BRAND LOGO_[0]', String(500)),
    Column('BRAND BANNER', String(500)),
    Column('BRAND VIDEO 1', String(500)),
    Column('BRAND VIDEO 2', String(500)),
    Column('WHEEL DESCRIPTION', String(500)),
    Column('SEO KEYWORDS', String(500)),
    Column('GROUP IDENTIFIER', String(500)),
    PrimaryKeyConstraint('SKU CODE (UNIQUE)', 'WHEEL OWNER')
)