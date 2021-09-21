from sqlalchemy import MetaData, Table, Column, SmallInteger, String, Float, PrimaryKeyConstraint
import pysftp
import warnings

warnings.filterwarnings('ignore')

# MySQL database details
db_conn_config = {
    'user': 'Giulio',
    'password': 'Capuozz0123!',
    'host': 'localhost',
    'database': 'dgt_database'
}

# WP SFTP server details
wp_conn_config = {
    'host': 'sftp.wheelpros.com',
    'username': 'Dgt_wheels1',
    'password': 'Alphabravo01!',
}
wp_remote_path = "/CommonFeed/EUR/WHEEL/wheelInvPriceData.csv"

# Japan Racing url with api key to get product list
jr_url = 'https://b2b.wheeltrade.pl/en/xmlapi/12/2/utf8/ee612fdd-4845-4c4e-b795-249514fc961f'

# DGT SFTP server details
ecom_conn_config = {
    'host': '136.244.69.20',
    'username': 'csvsftpuser',
    'password': 'Y8ZQ4[QMP[?FobU#!pWW',
}
ecom_remote_path = "/home/csvsftpuser/master_stock_list.csv"
# Disable hot key checking
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Suppliers list
suppliers_list = {
    'WHEEL PROS': 'WP',
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