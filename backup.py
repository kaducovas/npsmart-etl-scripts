import os
from ftplib import FTP
from datetime import date
import tarfile

backupdir = '/etl/scripts/'
outdir ='backup_etl/'
file = 'scripts200_'+str(date.today())+'.tar.gz'

###COMPRESS DIR
tar = tarfile.open(backupdir+file, "w:gz")
tar.add(backupdir, arcname="scripts_200")
tar.close()

###CONNECT & SEND FILE
session = FTP('172.29.200.201','postgres','Claro123')
uploadfile = open(backupdir+file,'rb')                  # file to send
session.storbinary('STOR '+outdir+file, uploadfile)     # send the file
uploadfile.close()
session.quit()

###REMOVE FILE
os.remove(backupdir+file)
