from ftplib import FTP
import psycopg2
import os
import subprocess
from ftplib import all_errors
import telepot
import emoji

dir = "/usr/bin/yowsup-master/"
bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
OK =  emoji.emojize(':heavy_check_mark:')
NOK = emoji.emojize(':cross_mark:') 
OK = ''
NOK = ''

db_conn = psycopg2.connect("dbname='postgres' user='postgres' host='172.29.200.201' password='Claro123'")
cursor = db_conn.cursor()
print('Connected to the database')

query = "SELECT MAX(ftp) FROM umts_control.log_etl WHERE oss = '15'"
cursor.execute(query)
file_15 = [item[0] for item in cursor.fetchall()]

query = "SELECT MAX(ftp) FROM umts_control.log_etl WHERE oss = '40'"
cursor.execute(query)
file_40 = [item[0] for item in cursor.fetchall()]

query = "SELECT MAX(ftp) FROM umts_control.log_etl WHERE oss = 'ATAE'"
cursor.execute(query)
file_ATAE = [item[0] for item in cursor.fetchall()]

query = "SELECT MAX(ftp) FROM lte_control.log_etl"
cursor.execute(query)
file_LTE = [item[0] for item in cursor.fetchall()]

cursor.close()

try:
	ftp = FTP('10.119.90.15')
	ftp.login('ftpuser','ftpuser')
except all_errors:
	message_15 = 'Connection with server 15 via FTP is not working. %s\nLast downloaded file was in %s' % (NOK,file_15[0])
else:
	message_15 = 'Connection with server 15 via FTP is working. %s\nLast downloaded file was in %s' % (OK,file_15[0])
	ftp.quit()

try:
	ftp = FTP('10.119.90.40')
	ftp.login('ftpuser','ftpuser')
except:
	message_40 = 'Connection with server 40 via FTP is not working. %s\nLast downloaded file was in %s' % (NOK,file_40[0])
else:
	message_40 = 'Connection with server 40 via FTP is working. %s\nLast downloaded file was in %s' %(OK,file_40[0])
	ftp.quit()

try:
	ftp = FTP('10.123.246.30')
	ftp.login('ftpuser','Changeme_123')
except:
	message_ATAE = 'Connection with server ATAE via FTP is not working. %s\nLast downloaded file was in %s' % (NOK,file_ATAE[0])
else:
	message_ATAE = 'Connection with server ATAE via FTP is working. %s\nLast downloaded file was in %s' % (OK,file_ATAE[0])
	ftp.quit()

try:
        ftp = FTP('10.123.246.10')
        ftp.login('ossuser','Changeme_123')
except:
        message_LTE = 'Connection with server LTE via FTP is not working. %s\nLast downloaded file was in %s' % (NOK,file_LTE[0])
else:
        message_LTE = 'Connection with server LTE via FTP is working. %s\nLast downloaded file was in %s' % (OK,file_LTE[0])
        ftp.quit()

message = message_15+'\n\n'+message_40+'\n\n'+message_ATAE+'\n\n'+message_LTE

print(message)

#subprocess.call([dir+"yowsup-cli", "demos", "-l", "5521981601755:ncphLavpww3Hxs7kZ5l9T9JWCeE=", "-s", "5521993094645-1444371705", message, "-M"])
bot.sendMessage('@NPSmart2', message)