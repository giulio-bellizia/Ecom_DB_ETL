# Ecom_DB_ETL
This project defines the architecture of a MySQL database of an ecommerce portal.

The database product list is created using data extracted from remote repositories of three suppliers via SFTP, HTTPS and an API made available by one of the suppliers.

The suppliers' product lists are transformed to conform the database format through pandas dataframe manipulations.

The transformed product lists are then loaded into the database. The interface with the database is handled using the SQLAlchemy package.