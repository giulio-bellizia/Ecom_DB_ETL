# this module connects to the supplier server, retrieves
# the updated product list and transforms it according to
# the master stock list format
import requests
import pandas as pd
import numpy as np
import io
from sqlalchemy import delete
from my_data import suppliers_list

# EXTRACT: connect to server via HTTPS and import updated product table into a dataframe
def wr_extr(url):
    wr_list = requests.get(url)
    wr_file = io.StringIO(wr_list.content.decode('utf-8'))
    product_list = pd.read_csv(wr_file)
    return product_list

# TRANSFORM: rename/transform/add/drop columns as per database table
def wr_xfrm(df):
    col_names = {
        'Total stock': 'QUANTITY (SETS AVAILABLE)',
        'sku': 'SKU CODE (UNIQUE)',
        'design': 'WHEEL MODEL',
        'brand': 'BRAND',
        'color': 'COLOUR',
        'width': 'J WIDTH',
        'diameter': 'SIZE',
        'wheelSize': 'SIZE DESC',
        'offset': 'ET',
        'pcd': 'PCD',
        'loadRating': 'WEIGHT LOAD (KG)',
        'centreBore': 'CB',
        'weight': 'WHEEL WEIGHT (KG)',
        'retailIncVat': 'MSRP',
        'image url': 'IMAGE 1 URL',
    }
    # rename columns
    df.rename(columns=col_names, inplace=True)
    # combine PCD and pcd_2 in one column
    df['pcd_2'] = df['pcd_2'].fillna('')
    df['PCD'] = np.where(df['pcd_2'], df['PCD'] + '|' + df['pcd_2'], df['PCD'])
    # drop non-relevant columns
    df = df[list(col_names.values())]
    # add and transform some columns
    def sd_convert(my_str):
        my_str = my_str.split('x')[1] + 'x' + my_str.split('x')[0]
        return my_str
    df['SIZE DESC'] = df['SIZE DESC'].apply(sd_convert)
    df['ITEM CODE'] = 'WR-' + df['SKU CODE (UNIQUE)']
    df['IMAGE SKU 1'] = df['ITEM CODE']
    df['IMAGE SOURCE'] = 'EXTERNAL_1'
    df['WHEEL OWNER'] = suppliers_list['WR']
    df['STOCK STATUS'] = 'PRE-ORDER'
    df['PRICE MARK UP'] = 30
    df['IMPORT / DISPLAY FILTER'] = 'TRUE'
    df['GROUP IDENTIFIER'] = df['BRAND'] + ' ' + df['WHEEL MODEL'] + ' ' + df['COLOUR']
    df['TOTAL UNIQUE PRICE (MSRP + MARGIN)'] = df['MSRP'] + df['PRICE MARK UP']
    df['SHIPPING (DOMESTIC)'] = 30
    df['PCD'] = df['PCD'].str.replace('x', '/')
    # drop duplicates with same SKU code
    df = df.drop_duplicates(subset=['SKU CODE (UNIQUE)'], keep='first')
    return df

# Update the database
def wr_update(url,db_engine,db_table,fn_extr, fn_xfrm):
    # Extract latest product list from suppliers
    df_extr = fn_extr(url)
    # Transform imported supplier product list to fit master stock list
    df_extrxfrm = fn_xfrm(df_extr)
    # Delete values from old supplier list from table
    stmt = delete(db_table).where(db_table.c['WHEEL OWNER'] == suppliers_list['WR'])
    with db_engine.begin() as conn:
        conn.execute(stmt)
    # Load the updated supplier list into the database
    df_extrxfrm.to_sql(db_table.name, con=db_engine, if_exists='append', index=False, chunksize=1024)
    print("Database updated with latest WR products")

# below some code for testing purposes
# df = wr_extr(wr_url)
# df = wr_xfrm(df)
# df.to_csv('wr_test', index=False)


