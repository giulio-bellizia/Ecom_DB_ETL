# this module connects to the supplier server, retrieves
# the updated product list and transforms it according to
# the master stock list format

import pysftp
import pandas as pd
import sqlalchemy

# EXTRACT: connect to server and retrieve updated table
# SFTP server details
wp_conn_config = {
    'host': 'sftp.wheelpros.com',
    'username': 'Dgt_wheels1',
    'password': 'Alphabravo01!',
}
wp_remote_path = "/CommonFeed/EUR/WHEEL/wheelInvPriceData.csv"
# Disable hot key checking
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# Connect to SFTP server and import data into a dataframe
def wp_extr(connection_config, cnopts, remote_path):
    print("Connecting to {}...".format(connection_config['host']), end='')
    with pysftp.Connection(**connection_config, cnopts=cnopts) as mysftp:
        if mysftp.exists(remote_path):
            print("{} found.".format(remote_path))
        # copy destination file into a pandas dataframe
        with mysftp.open(remote_path, bufsize=32768) as csv_file:
            print("Importing file...", end='')
            product_list = pd.read_csv(csv_file)
            print("{} imported.".format(remote_path))
            mysftp.close()
    return product_list

# TRANSFORM: modify table to conform with the master
# stock list table in the database
def wp_xfrm(df):
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
    return df