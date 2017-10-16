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

bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
OK =  emoji.emojize(':heavy_check_mark:')
start_time = time.time()

#####SET DIR
current_date = time.strftime("%Y%m%d")
indir = '/etl/NPM/Dumps/CFGMML/'+str(current_date)+'/'
#indir = '/home/etluser/npm/dumps/cfgmml/'+str(current_date)+'/'

#outdir = '/etl/NPM/Dumps/CFGMML/temp/'
outdir = '/home/etluser/npm/dumps/cfgmml/temp/'
#backupdir = 'C:/Users/c00310965/Desktop/teste/CFG/backup/'

#configurationdir = '/etl/NPM/Dumps/CFGMML/'+current_date+'/configuration/'
configurationdir = '/home/etluser/npm/dumps/cfgmml/'+current_date+'/configuration/'

#####Connect to the database92
db_conn = psycopg2.connect("dbname='postgres' user='postgres' host='172.29.200.201' password='Claro123'")
cursor = db_conn.cursor()
print('Connected to the database')

###query available tables
query = "SELECT distinct table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'umts_configuration' and table_name not in ('parameters') and table_name not like '%_history' order by table_name"
cursor.execute(query)
db_conn.commit()
tables = [item[0] for item in cursor.fetchall()]
tables = [x.upper() for x in tables]


#####Extract .tar.gz
for dir in os.listdir(indir):
	for file in os.listdir(indir+'/'+dir+'/'):
			print('Extracting file '+file)
			zip = zipfile.ZipFile(indir+'/'+dir+'/'+file)
			zip.extractall(indir+'/'+dir+'/')
			file = zip.namelist()[0]

	#####get rncid and datetime from filename
			rncid = file.split('-')[1][3:]
			datetime = file.split('-')[3][:14]
			datetime = (datetime[0:4] + '-' + datetime[4:6] + '-' + datetime[6:8] + ' ' + datetime[8:10] + ':' + datetime[10:12] + ':' + datetime[12:14])
			#print(file)

	#####Parse CFG for all rncs in folder and format for postgresql copy
			
			print('Parsing '+file)
			ifile  = open(indir+'/'+dir+'/'+file, "r",newline="\n", encoding="ISO-8859-1")
			reader = csv.reader(ifile, delimiter=',')
			#ofile  = open(outdir+'import_'+file, "w", newline="\n", encoding="utf-8")
			#writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

			rncname = list(ifile)[8].split(',')[1].split('=')[1]
			#print(rncname)
			ifile.seek(0)
			
			for i in range(8): next(reader) # skipt first 8 lines

	#        for row in reader:
	 #               print(row[1])
	 #               break
			
		  #  for row in reader:
		   #         print(row)
			#        break
			#print(reader)
			#rncname = list(ifile)[0]
			#print(rncname)
			
			for key, rows in groupby(reader,lambda row: row[0].split(':')[0].split(' ')[0]+row[0].split(':')[0].split(' ')[1]):
					#print(key)
					if key[3:] in tables and key[:3] != 'ACT':# or key[3:] == 'UCELL':
		 
							##query columns for fieldname of dictwriter
							table_name = key[3:].lower()
							query = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'umts_configuration' and table_name = '"+table_name+"'" 
							#print('Executing: '+query+'in PostgreSQL')
							cursor.execute(query)
							db_conn.commit()
							columns = [item[0] for item in cursor.fetchall()]
							columns = [x.upper() for x in columns]
					
							with open(outdir+"%s.csv" % table_name, "a", newline="\n", encoding="UTF-8") as output:
									#writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
									writer = csv.DictWriter(output, fieldnames=columns, extrasaction='ignore')
									for row in rows:
											row.insert(0,"RNCNAME="+rncname)                                        
											row.insert(0,"RNCID="+rncid)
											row.insert(0,"DATETIME="+datetime)
											row = [r.replace(";","") for r in row]
											row = [r.replace('"','') for r in row]
											row = [r.strip() for r in row]                                        
											row[3] = row[3].split(':')[1] ###index of MO infoafter being shifted right 3 positions
											###
											#print(row)
											dict = {k:v for k,v in (x.split('=') for x in row) }
											#writer.writerow(row)
											writer.writerow(dict)                                           										
									#writer.writeheader()

							output.close()
			ifile.close()                        
			os.remove(indir+'/'+dir+'/'+file)
timestamp = (time.time() - start_time)
print("CFGMMLs took " +str(timestamp)+ " seconds to be parsed.")  
                         

#################COPY#################


######Truncate tables

for file in os.listdir(outdir):
    copy_time = time.time()
    table_name = 'umts_configuration.'+file[:-4]

    query = "truncate table "+table_name
    cursor.execute(query)
    db_conn.commit()

#####execute copy
    csvfile = open(outdir+file)
    SQL_STATEMENT = "COPY %s FROM STDIN WITH CSV DELIMITER AS ',' NULL AS ''"
    table_name_history = table_name+'_history'

    try:
        print("Executing Copy in "+table_name)
        cursor.copy_expert(sql=SQL_STATEMENT % table_name, file=csvfile)         
        ###db_conn.commit()
        copytimestamp = (time.time() - copy_time)
        print(" Copy took " +str(copytimestamp)+ " seconds to run for "+ table_name)
    except psycopg2.IntegrityError:
        db_conn.commit()
        csvfile.close()	        		
    else:
        db_conn.commit()
        csvfile.close()
        #os.rename(outdir+file, backupdir+file)
        #shutil.copyfile(outdir+file, backupdir+file)
		
    # csvfile = open(outdir+file)
    # try:
        # print("Executing Copy in "+table_name_history)
        # cursor.copy_expert(sql=SQL_STATEMENT % table_name_history, file=csvfile)    
        # ###db_conn.commit()
        # copytimestamp = (time.time() - copy_time)
        # print(" Copy took " +str(copytimestamp)+ " seconds to run for "+ table_name_history)
    # except psycopg2.IntegrityError:
        # db_conn.rollback()
        # csvfile.close()
    # else:
        # db_conn.commit()
        # csvfile.close()

if not os.path.exists(configurationdir):
	os.makedirs(configurationdir)

for file in os.listdir(outdir):
    #print(file[:-4])
    query = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'umts_configuration' and table_name = '"+str(file[:-4])+"'"
    cursor.execute(query)
    db_conn.commit()
    columns = [item[0] for item in cursor.fetchall()]
    header = ','.join(columns)
    with open(outdir+file, 'r') as original: data = original.read()
    with open(configurationdir+file, 'w') as modified: modified.write(header+'\n'+data)
    original.close()
    modified.close()
    os.remove(outdir+file)    

cursor.close()
db_conn.close()
print("Inicio do missing_cells_on_mo")
subprocess.call("python3.4 /etl/scripts/missing_cells_on_mo.py",shell=True)
print("Término do missing_cells_on_mo")
print("Inicio do consistency_check")
subprocess.call("python3.4 /etl/scripts/consistency_check.py",shell=True)
print("Término do consistency_check")
# print("Inicio do inserir_configuration_history")
subprocess.call("/etl/scripts/inserir_configuration_history.sh",shell=True)
# print("Término do inserir_configuration_history")

timestamp = (time.time() - start_time)
print(" Script took " +str(timestamp)+ " seconds to finish")
bot.sendMessage('@NPSmart2', 'cfg.py finished '+OK)	
#os.system("python3.4 /etl/scripts/parameters2json_rnc.py")
