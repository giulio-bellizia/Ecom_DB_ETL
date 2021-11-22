# this module connects to the supplier server, retrieves
# the updated product list and transforms it according to
# the master stock list format
import pysftp
import os
import pandas as pd
from sqlalchemy import delete
from my_data import suppliers_path, suppliers_list

# EXTRACT: connect to server via SFTP and import csv product table into a local file and a dataframe
def wp_extr(connection_config, cnopts, remote_path):
    print("Connecting to {}...".format(connection_config['host']), end='')
    with pysftp.Connection(**connection_config, cnopts=cnopts) as mysftp:
        if mysftp.exists(remote_path):
            print("{} found.".format(remote_path))
        # copy destination file into a pandas dataframe
        with mysftp.open(remote_path, bufsize=32768) as url_file:
            print("Importing latest data from supplier...", end='')
            product_list = pd.read_csv(url_file)
            print("{} imported.".format(remote_path))
        # copy destination file into a local file
        os.makedirs(suppliers_path, exist_ok=True)
        mysftp.get(remote_path, os.path.join(suppliers_path, '{}_raw_file.csv'.format(suppliers_list['WP'])))
    return product_list

# TRANSFORM: rename/transform/add/drop columns as per database table
def wp_xfrm(df):
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
    df['SIZE DESC'] = df['SIZE DESC'].str.replace('X','x')
    df['WHEEL OWNER'] = suppliers_list['WP']
    df['SIZE'] = df['SIZE DESC'].str[:2]
    df['J WIDTH'] = df['SIZE DESC'].str.split('x').str[-1]
    df['SHIPPING (DOMESTIC)'] = 30
    df['PRICE MARK UP'] = 0
    df['TOTAL UNIQUE PRICE (MSRP + MARGIN)'] = df['MSRP']+df['PRICE MARK UP']
    df['IMPORT / DISPLAY FILTER'] = 'TRUE'
    df['GROUP IDENTIFIER'] = df['BRAND']+' '+df['WHEEL MODEL']+' '+df['COLOUR']
    df['ITEM CODE'] = 'WP-' + df['SKU CODE (UNIQUE)']
    df['IMAGE SKU 1'] = df['ITEM CODE']
    df['ET'] = df['ET'].str.lstrip('0')
    df['ET'] = df['ET'].str.replace('XX', 'Custom')
    def PCD_convert(my_str):
        if 'X' in my_str:
            if '/' in my_str:
                my_str = my_str.split('/')[0]+'/' + my_str.split('X')[0]+'X' + my_str.split('/')[1]
                my_str = my_str.replace('/', '|')
                my_str = my_str.replace('X', '/')
            else:
                my_str = my_str.replace('X', '/')
            my_str = [list(map(float, sublist.split('/'))) for sublist in my_str.split('|')]
            my_str = [[x[0], round(x[1] * 25.4,2)] if x[1] < 50 else [x[0], x[1]] for x in my_str]
            my_str = '|'.join(['/'.join(map(str, sublist)) for sublist in my_str]).replace('.0', '')
            my_str = my_str.replace('107.95','108')
        return my_str
    df['PCD'] = df['PCD'].apply(PCD_convert)
    return df

# Update the database
def wp_update(conn_config,cnopts,remote_path,db_engine,db_table,fn_extr, fn_xfrm):
    # Extract latest product list from suppliers
    df_extr = fn_extr(conn_config, cnopts, remote_path)
    # Transform imported supplier product list to fit master stock list
    df_extrxfrm = fn_xfrm(df_extr)
    # Delete values from old supplier list from table
    stmt = delete(db_table).where(db_table.c['WHEEL OWNER'] == suppliers_list['WP'])
    with db_engine.begin() as conn:
        conn.execute(stmt)
    # Load the updated supplier list into the database
    df_extrxfrm.to_sql(db_table.name, con=db_engine, if_exists='append', index=False, chunksize=1024)
    print("Database updated with latest WP products")
