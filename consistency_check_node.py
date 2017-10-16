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

#####Connect to the database92
db_conn = psycopg2.connect("dbname='postgres' user='postgres' host='172.29.200.201' password='Claro123'")
cursor = db_conn.cursor()
print('Connected to the database')

###BASELINE NODEB NOK
query = "copy(select * from umts_baseline.baseline_audit_node('baseline_nodeb') where status = 'NOK') to '"+dirout_db+"baseline_nodeb.txt';"
cursor.execute(query)
db_conn.commit()

query = "copy umts_baseline.consistency_check_node_nok_hist from '"+dirout_db+"baseline_nodeb.txt';"
cursor.execute(query)
db_conn.commit()
	
cursor.close()
db_conn.close()
bot.sendMessage('@NPSmart2', 'larga de ser burro rapá. salva a parada. baseline_nodeb rodou agora '+OK)	
