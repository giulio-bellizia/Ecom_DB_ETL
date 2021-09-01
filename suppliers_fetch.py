# this module fetches data from suppliers
# establish connection to server
# fetch data
# to dos: implement password security, RSA DSA, handling passords safely in python

import pysftp

# import sys
# path = './THETARGETDIRECTORY/' + sys.argv[1]    #hard-coded
# localpath = sys.argv[1]

# address and login details of teh SFTP site
host = "sftp.wheelpros.com"     #hard-coded
username = "Dgt_wheels1"                #hard-coded
password = "Alphabravo01!"                #hard-coded

# Disable hot key checking - it could be re-implemented later
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

remote_path = "/CommonFeed/EUR/WHEEL/wheelInvPriceData.csv"
# establish connection to SFTP server
with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
    if sftp.exists(remote_path):
        print("it exists!")
    # sftp.listdir_attr(/)
    # sftp.put(localpath, path)

sftp.close()  # Close connection

print("Upload done.")


# data = srv.listdir()  # Get the directory and file listing in a list
# srv.get(file_path)  # Download a file from remote server
# srv.execute('pwd') # Execute a command on the server

# cinfo = {'host':'hostname', 'username':'me', 'password':'secret', 'port':2222}
# with pysftp.Connection(**cinfo) as sftp:
    #
    # ... do sftp operations
    #

# copy all files under public to a local path, preserving modification time
# sftp.get_d('public', 'local-backup', preserve_mtime=True)

# copy all files AND directories under public to a local path
# sftp.get_r('public', 'local-backup', preserve_mtime=True)


# >>> sftp.exists('readme.txt')   # a file
# True
# >>> sftp.exists('pub')          # a dir
# True

# path = "sftp://user:p@ssw0rd@test.com/path/to/file.txt"

# Read a file
# with open_sftp(path) as f:
#     s = f.read()
# print s
#
# # Write to a file
# with open_sftp(path, mode='w') as f:
#     f.write("Some content.")