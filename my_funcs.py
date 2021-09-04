from my_data import db_conn_config
from sqlalchemy_utils import database_exists, create_database

# return engine once database is either found or created
def conn_db_create(db_conn):
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