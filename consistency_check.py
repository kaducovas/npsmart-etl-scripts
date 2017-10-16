import os
import sys
import csv
import time
import zipfile
import psycopg2
import re
import shutil
from itertools import groupby
import telepot
import emoji
import subprocess
import pysftp

bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
OK =  emoji.emojize(':heavy_check_mark:')
start_time = time.time()



#####SET DIR
current_date = time.strftime("%Y%m%d")
indir = '/etl/NPM/Dumps/CFGMML/'+str(current_date)+'/consistency_check/'
dirout = '/var/www/html/npsmart/output/'
dirout_db = '/home/postgres/temp/baseline/'
dirmml = '/ftproot/Scripts/Custom/Consistency_check/'

if not os.path.exists(indir):
	os.makedirs(indir)

#####Connect to the database92
db_conn = psycopg2.connect("dbname='postgres' user='postgres' host='172.29.200.201' password='Claro123'")
cursor = db_conn.cursor()
print('Connected to the database')

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

###BASELINE NOK
query = "select * from umts_baseline.baseline_audit('baseline') where status = 'NOK'"
outputquery = "copy ({0}) to STDOUT WITH CSV HEADER".format(query)
	
with open(indir+'baseline_nok.csv','a') as f:
	cursor.copy_expert(outputquery,f)
cursor.execute(query)
f.close()

session = pysftp.Connection('172.29.200.203',username='webadmin',password='Claro123',cnopts=cnopts)
with session.cd(dirout): #chdir to public
	session.put(indir+'baseline_nok.csv') #upload file to nodejs/
	session.chmod(dirout+'baseline_nok.csv',777)
	
session = pysftp.Connection('172.29.200.201',username='postgres',password='Claro123',cnopts=cnopts)
with session.cd(dirout_db): #chdir to public
	session.put(indir+'baseline_nok.csv') #upload file to nodejs/
	session.chmod(dirout_db+'baseline_nok.csv',777)
	session.execute('/home/postgres/scripts/baseline_nok_daily.sh')
	
bot.sendMessage('@NPSmart2', 'Baseline NOK finished '+OK)	

###BASELINE COUNT
query = "select * from umts_baseline.vw_baseline_class_daily"
outputquery = "copy ({0}) to STDOUT WITH CSV HEADER".format(query)
	
with open(indir+'baseline_count.csv','a') as f:
	cursor.copy_expert(outputquery,f)
cursor.execute(query)
f.close()

session = pysftp.Connection('172.29.200.201',username='postgres',password='Claro123',cnopts=cnopts)
with session.cd(dirout_db): #chdir to public
	session.put(indir+'baseline_count.csv') #upload file to nodejs/
	session.chmod(dirout_db+'baseline_count.csv',777)
	session.execute('/home/postgres/scripts/baseline_count_daily.sh')

bot.sendMessage('@NPSmart2', 'Baseline Count finished '+OK)
	
###BASELINE NOK AUTOMML	
query = "select * from umts_baseline.baseline_audit_automml('baseline') where status = 'NOK'"
outputquery = "copy ({0}) to STDOUT WITH CSV HEADER".format(query)
	
with open(indir+'baseline_nok_automml.csv','a') as f:
	cursor.copy_expert(outputquery,f)
cursor.execute(query)
f.close()

session = pysftp.Connection('10.119.232.5',username='ftpuser',password='Changeme_123',cnopts=cnopts)
with session.cd(dirmml): #chdir to public
	session.put(indir+'baseline_nok_automml.csv') #upload file to nodejs/
	session.chmod(dirmml+'baseline_nok_automml.csv',777)
#	#session.close()

session2 = pysftp.Connection('10.123.246.30',username='ftpuser',password='Changeme_123',cnopts=cnopts)
with session2.cd(dirmml): #chdir to public
	session2.put(indir+'baseline_nok_automml.csv') #upload file to nodejs/
	session2.chmod(dirmml+'baseline_nok_automml.csv',777)
	#session.close()

bot.sendMessage('@NPSmart2', 'Baseline Auto MML finished '+OK)

cursor.close()
db_conn.close()
bot.sendMessage('@NPSmart2', 'Consistency Check finished '+OK)	
