from ftplib import FTP
import psycopg2
import os
import subprocess
import telepot
import emoji

dir = '/usr/bin/yowsup-master/'
bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
NOK = emoji.emojize(':cross_mark:')
WARNING = emoji.emojize(':warning_sign:')

db_conn = psycopg2.connect('dbname=\'postgres\' user=\'postgres\' host=\'172.29.200.201\' password=\'Claro123\'')
cursor = db_conn.cursor()
print('Connected to the database')

query = 'SELECT ftp FROM umts_control.log_etl where oss = \'15\' AND not ftp is null order by ftp desc limit 1'
cursor.execute(query)
file_15 = str([item[0] for item in cursor.fetchall()][0])

#query = 'SELECT ftp FROM umts_control.log_etl where oss = \'40\' AND not ftp is null order by ftp desc limit 1'
#cursor.execute(query)
#file_40 = str([item[0] for item in cursor.fetchall()][0])

query = 'SELECT ftp FROM umts_control.log_etl where oss = \'ATAE\' AND not ftp is null order by ftp desc limit 1'
cursor.execute(query)
file_ATAE = str([item[0] for item in cursor.fetchall()][0])

query = 'SELECT ftp FROM lte_control.log_etl WHERE oss = \'10\' AND not ftp is null order by ftp desc limit 1'
cursor.execute(query)
file_LTE = str([item[0] for item in cursor.fetchall()][0])

cursor.close()

try:
	ftp = FTP('10.119.90.15')
	ftp.login('ftpuser','ftpuser')
except:
	message_15 = 'Connection with server 15 via FTP is not working.\nLast downloaded file was in '+file_15
else:
	message_15 = '' 
	ftp.quit()

#try:
#	ftp = FTP('10.119.90.40')
#	ftp.login('ftpuser','ftpuser')
#except:
#	message_40 = 'Connection with server 40 via FTP is not working.\nLast downloaded file was in '+file_40
#else:
#	message_40 = ''
#	ftp.quit()

try:
	ftp = FTP('10.123.246.30')
	ftp.login('ftpuser','Changeme_123')
except:
	message_ATAE = 'Connection with server ATAE via FTP is not working.\nLast downloaded file was in '+file_ATAE
else:
	message_ATAE = ''
	ftp.quit()

try:
        ftp = FTP('10.123.246.10')
        ftp.login('ftpuser','Changeme_123')
except:
        message_LTE = 'Connection with server LTE via FTP is not working.\nLast downloaded file was in '+file_LTE
else:
        message_LTE = ''
        ftp.quit()

message = message_15+message_ATAE+message_LTE

if message:
	message='\n\n'.join([item for item in (message_15,message_ATAE,message_LTE) if item])

	print(message)

	#subprocess.call([dir+'yowsup-cli', 'demos', '-l', '5521981601755:ncphLavpww3Hxs7kZ5l9T9JWCeE=', '-s', '5521993094645-1444371705', message, '-M'])
	bot.sendMessage('@NPSmart2', 'WARNING '+WARNING+'\n\n'+message)
