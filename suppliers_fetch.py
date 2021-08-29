# this module fetches data from suppliers
# establish connection to server
# fetch data
# to dos: implement password security

import pysftp
import sys

path = './THETARGETDIRECTORY/' + sys.argv[1]    #hard-coded
localpath = sys.argv[1]

host = "THEHOST.com"                    #hard-coded
password = "THEPASSWORD"                #hard-coded
username = "THEUSERNAME"                #hard-coded

with pysftp.Connection(host, username=username, password=password) as sftp:
    sftp.put(localpath, path)

print 'Upload done.'

data = srv.listdir()  # Get the directory and file listing in a list
srv.get(file_path)  # Download a file from remote server
srv.execute('pwd') # Execute a command on the server

import pysftp
cinfo = {'host':'hostname', 'username':'me', 'password':'secret', 'port':2222}
with pysftp.Connection(**cinfo) as sftp:
    #
    # ... do sftp operations
    #

# copy all files under public to a local path, preserving modification time
sftp.get_d('public', 'local-backup', preserve_mtime=True)

# copy all files AND directories under public to a local path
sftp.get_r('public', 'local-backup', preserve_mtime=True)

...
>>> sftp.exists('readme.txt')   # a file
True
>>> sftp.exists('pub')          # a dir
True