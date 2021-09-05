# this module fetches data from suppliers
# transform it in the needed format and
# load it in the database
# to dos: implement password security, RSA DSA, handling passwords safely in python

import pysftp
import pandas as pd
import sqlalchemy

# EXTRACT: connect to server and retrieve updated table

# specify SFTP server details
connection_config = {
    'host': 'sftp.wheelpros.com',
    'username': 'Dgt_wheels1',
    'password': 'Alphabravo01!',
}
remote_path = "/CommonFeed/EUR/WHEEL/wheelInvPriceData.csv"

# Disable hot key checking - it could be re-implemented later
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# # establish connection to SFTP server
# print("Connecting to {}...".format(wp_conn_config['host']))
# with pysftp.Connection(**wp_conn_config, cnopts=cnopts) as mysftp:
#     if mysftp.exists(wp_remote_path):
#         print("Destination file found!")
#     # copy destination file into a pandas dataframe
#     with mysftp.open(wp_remote_path) as csv_file:
#         print("Copying destination file...")
#         df = pd.read_csv(csv_file)
#         print("destination file in memory.")
#         mysftp.close()

# TRANSFORM: modify table to the sql table format
df = pd.read_csv("wheelInvPriceData.csv")

# rename columns as per table in database and drop columns not renamed
col_names = {
    'PartNumber':       'SKU CODE (UNIQUE)',
    'ImageURL':         'IMAGE 1 URL',
    'Brand':            'BRAND',
    'ModelName':        'WHEEL MODEL',
    'Size':             'SIZE DESC',
    'BoltPattern':      'PCD',
    'Offset':           'ET',
    'CenterBore':       'CB',
    'Finish':           'COLOUR',
    'LoadRating':       'WEIGHT LOAD (KG)',
    'ShippingWeight':   'WHEEL WEIGHT (KG)',
    'TotalQOH':         'QUANTITY (SETS AVAILABLE)',
    'MSRP':             'MSRP',
}
df.rename(columns=col_names, inplace=True)
df = df[ list(col_names.values()) ]

# insert certain columns not originally in the supplier table
df['WHEEL OWNER'] = 'WHEEL PROS'
df['SIZE'] = df['SIZE DESC'].str[:2]
df['J WIDTH'] = df['SIZE DESC'].str.split('X').str[-1]
df['SHIPPING (DOMESTIC)'] = 30
df['PRICE MARK UP'] = 0
df['TOTAL UNIQUE PRICE (MSRP + MARGIN)'] = df['MSRP']+df['PRICE MARK UP']
df['IMPORT / DISPLAY FILTER'] = 'TRUE'
df['GROUP IDENTIFIER'] = df['BRAND']+' '+df['WHEEL MODEL']+' '+df['COLOUR']
df['ITEM CODE'] = 'WP-' + df['SKU CODE (UNIQUE)']
df['IMAGE SKU 1'] = df['ITEM CODE']
def PCD_convert(my_str):
    if 'X' in my_str:
        if '/' in my_str:
            my_str = my_str.split('/')[0]+'/' + my_str.split('X')[0]+'X' + my_str.split('/')[1]
            my_str = my_str.replace('/', '|')
            my_str = my_str.replace('X', '/')
        else:
            my_str = my_str.replace('X', '/')
    return my_str
df['PCD'] = df['PCD'].apply(PCD_convert)

# for col in df.columns:
#     print(col)
# pd.set_option( "display.max_columns", None)
# print(df)
# for col in df.columns:
#     print(col)

# LOAD: connect to the MySQL database and update the master stock list
# specify MySQL server details
connection_config = {
    'host': 'localhost',
    'user': 'Giulio',
    'password': 'Capuozz0123!',
    'database': 'dgt_database',
}

# provide the name for the database

# my_str = 'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('Giulio','Capuozz0123!','localhost','dgt_database')
# print(my_str)
# print(df.dtypes)
# engine = sqlalchemy.create_engine('mysql+mysqlconnector://localhost:Giulio@Capuozz0123!/dgt_database')
# dialect+driver://username:password@host:port/database

engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('Giulio','Capuozz0123!','localhost','dgt_database'), pool_pre_ping=True)
# engine.execute('set max_allowed_packet=67108864')
df = df.head(2000)
df.to_sql('master_stock_list', con=engine, if_exists='append',index=False)

query = 'select * from master_stock_list'
results = pd.read_sql_query(query, engine)
results.to_csv("wheelpros.csv", index=False)