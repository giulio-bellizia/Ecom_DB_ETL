# this module connects to the supplier server, retrieves
# the updated product list and transforms it according to
# the master stock list format
import requests
import pandas as pd
import numpy as np
import io
from sqlalchemy import delete
from my_data import suppliers_list

# EXTRACT: connect to server via HTTP and import updated product table into a dataframe
def ap_extr(url):
    ap_list = requests.get(url)
    ap_file = io.StringIO(ap_list.content.decode('utf-8'))
    product_list = pd.read_csv(ap_file)
    return product_list

def ap_xfrm(df):
    # TRANSFORM: rename/transform/add/drop columns as per database table
    col_names = {
        'UID': 'SKU CODE (UNIQUE)',
        'BRAND': 'BRAND',
        'IMG': 'IMAGE 1 URL',
        '360 IMAGE': 'VIDEO 1 URL',
        'DESIGN': 'WHEEL MODEL',
        'DIAMETER': 'SIZE',
        'ET': 'ET',
        'WIDTH': 'J WIDTH',
        'CB': 'CB',
        'COLOUR': 'COLOUR',
        'LOAD': 'WEIGHT LOAD (KG)',
        'TOTAL STOCK': 'QUANTITY (SETS AVAILABLE)',
        'PRICE (GBP)': 'MSRP',
        'PCD': 'PCD',
    }
    # rename columns
    df.rename(columns=col_names, inplace=True)

    # combine columns to create PCD field
    df['PCD'] = df['HOLES'].apply(str) + '/' + df['PCD'].apply(str)

    # drop non-relevant columns
    df = df[list(col_names.values())]

    # add and transform some columns
    df['ITEM CODE'] = 'AP-' + df['SKU CODE (UNIQUE)']
    df['IMAGE SKU 1'] = df['ITEM CODE']
    df['IMAGE SOURCE'] = 'EXTERNAL_1'
    df['WHEEL OWNER'] = suppliers_list['AP']
    df['J WIDTH'] = df['J WIDTH'].apply(str)
    df['J WIDTH'] = df['J WIDTH'].str.replace('\.0', '')
    df['SIZE DESC'] = df['SIZE'].apply(str) + 'x' + df['J WIDTH']
    df['SUPPLIER LOCATION'] = 'UNITED KINGDOM'
    df['PRICE MARK UP'] = 30
    df['MSRP'] = df['MSRP']*1.2
    df['TOTAL UNIQUE PRICE (MSRP + MARGIN)'] = df['MSRP'] + df['PRICE MARK UP']
    df['IMPORT / DISPLAY FILTER'] = 'TRUE'
    df['GROUP IDENTIFIER'] = df['BRAND'] + ' ' + df['WHEEL MODEL'] + ' ' + df['COLOUR']
    df['STOCK STATUS'] = 'PRE-ORDER'

    # drop duplicates with same SKU code
    df = df.drop_duplicates(subset=['SKU CODE (UNIQUE)'], keep='first')
    return df

# Update the database
def ap_update(url,db_engine,db_table,fn_extr, fn_xfrm):
    # Extract latest product list from suppliers
    df_extr = fn_extr(url)
    # Transform imported supplier product list to fit master stock list
    df_extrxfrm = fn_xfrm(df_extr)
    # Delete values from old supplier list from table
    stmt = delete(db_table).where(db_table.c['WHEEL OWNER'] == suppliers_list['AP'])
    with db_engine.begin() as conn:
        conn.execute(stmt)
    # Load the updated supplier list into the database
    df_extrxfrm.to_sql(db_table.name, con=db_engine, if_exists='append', index=False, chunksize=1024)
    print("Database updated with latest AP products")