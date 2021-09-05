from sqlalchemy_utils import database_exists, create_database
import pysftp

# return engine once database is either found or created
def conn_db_create(db_conn, db_conn_config):
    if not database_exists(db_conn.url):
        # Create database if it does not exists
        print('Database not found, creating database {} ...'.format(db_conn_config['database']), end='')
        create_database(db_conn.url)
        print("OK")
    else:
        # Connect the database if exists.
        print('Connecting to database {} ...'.format(db_conn_config['database']), end='')
        db_conn.connect()
        print("OK")
    return db_conn

# Connect to SFTP server and import data into a dataframe
def ecom_upload(connection_config, cnopts, remote_path, dataframe):
    print("Connecting to {}...".format(connection_config['host']), end='')
    with pysftp.Connection(**connection_config, cnopts=cnopts) as mysftp:
        print("connection established.")
        # upload product list to SFTP server
        with mysftp.open(remote_path, "w", bufsize=32768) as csv_file:
            print("Uploading to SFTP server...", end='')
            dataframe.to_csv(csv_file, index=False)
    return print("Upload to {} completed.".format(remote_path))