from ftplib import FTP
import psycopg2
import time
import datetime
import os
import shutil
import re

def getpm(ip,user,password,pmfolder,prefix):
	localdir = '/etl/lte/performance/temp/ftp/'
	finaldir = '/etl/lte/performance/special/'
	converteddir = '/etl/lte/performance/converted/'
	backupdir = '/etl/backup/lte/performance/'
	logfile = '/home/etluser/log/ftp-10.log'

	try:
		conn = psycopg2.connect("dbname='postgres' user='postgres' host='172.29.200.201' password='Claro123'")
	except:
		print ('db error')
	sqlloaded = "SELECT CONCAT(oss,'_',file) FROM lte_control.log_etl WHERE datetime > '2016-12-12' AND oss = '10';"
	sqlselected = "SELECT DISTINCT(functionsubset_id) FROM lte_control.counter_reference WHERE counter_id in (1526726657,1526726658,1526728217,1526728218,1526728219,1526728220,1526728221,1526728216,1526726659,1526728222,1526728223,1526728224,1526728225,1526728226,1526728357,1526728358,1526728438,1526728439,1526728774,1526728489,1526727084,1526728269,1526728490,1526732044,1526729949,1526727083,1526728485,1526728486,1526732920,1526732921,1526730846,1526728272,1526728273,1526728850,1526726668,1526726670,1526726672,1526726674,1526726678,1526726680,1526726682,1526726684,1526726676,1526726669,1526726671,1526726673,1526726675,1526726679,1526726681,1526726683,1526726685,1526726677,1526728274,1526728192,1526728200,1526728275,1526728193,1526728201,1526727544,1526727545,1526736847,1526736848,1526736849,1526736850,1526728776,1526728879,1526728276,1526728277,1526729951,1526729952,1526728278,1526726717,1526728279,1526729545,1526729546,1526729953,1526729954,1526729955,1526729956,1526728280,1526729950,1526730830,1526730831,1526732726,1526732922,1526732924,1526732926,1526732928,1526736694,1526736695,1526736696,1526736697,1526736698,1526736699,1526736856,1526736857,1526736869,1526728787,1526727215,1526727218,1526728932,1526727216,1526727219,1526727217,1526727220,1526727221,1526727222,1526727223,1526727224,1526727225,1526728954,1526728955,1526728937,1526728938,1526728939,1526730874,1526730875,1526728956,1526728957,1526728958,1526728959,1526728960,1526728961,1526728962,1526728963,1526728964,1526728965,1526728966,1526728967,1593835630,1593835632,1593835633,1593835634,1526726884,1526726885,1526726886,1526728337,1526728521,1526727212,1526727378,1526727379,1526728077,1526728467,1526727853,1526727854,1526727861,1526727862,1526728250,1526728251,1526728252,1526728253,1526727388,1526727389,1526728298,1526729957,1526729958,1526729959,1526729960,1526729961,1526729962,1526729963,1526729964,1526729965,1526729966,1526729967,1526729968,1526729969,1526729970,1526729971,1526727209,1526727210,1526728320,1526728465,1526728493,1526729659,1526729660,1526733199,1526728517,1526730878,1526732895,1526727253,1526727256,1526728334,1526737817,1526737818,1526737819);"
	cursor = conn.cursor()
	cursor.execute(sqlloaded)
	time.sleep(0.5)
	sqlloadedfiles = [item[0] for item in cursor.fetchall()]

	cursor.execute(sqlselected)
	time.sleep(0.5)
	sqlselectedsubset = [item[0] for item in cursor.fetchall()]
	ftp = FTP(ip,user,password)
	ftp.login()
	ftp.cwd(pmfolder)
	dirlist = ftp.nlst()

	for dirname in dirlist:
		matchdir = re.match('.*pmexport_.*',dirname)
		if matchdir:
			#print(dirname)
			ftp.cwd(pmfolder+dirname)
			filenames = ftp.nlst()
			filenames = sorted(filenames, key=lambda x: x.split("_")[3])
			for filename in filenames:
				#print(filename)
				OutputFilename = prefix + filename
				if OutputFilename not in sqlloadedfiles:
					for selection in sqlselectedsubset:
						matchfile = re.match('.*'+str(selection)+'.*',filename)
						if matchfile:
							#print(OutputFilename)
							if (os.path.exists(finaldir+OutputFilename) or os.path.exists(converteddir+OutputFilename+'.csv')):
								print('%s Exists' % OutputFilename)
							else:
								print ('Opening local file ' + OutputFilename)
								file = open(localdir +OutputFilename, 'wb')
								print ('Getting ' + OutputFilename)
								try:
									ftp.retrbinary('RETR %s' % filename, file.write)
									#cursor.execute('INSERT INTO lte_control.log_etl (oss,file,fss,datetime,ftp) VALUES (%s, %s, %s, %s, %s)',(prefix.split('_')[0],filename,filename.split('_')[1],filename.split('_')[4][0:4] + '-' + filename.split('_')[4][4:6] + '-' + filename.split('_')[4][6:8] + ' ' + filename.split('_')[4][8:10] + ':' + filename.split('_')[4][10:12] + ':00' ,str(datetime.datetime.now())[0:19]))
									#conn.commit()
									time.sleep(0.5)
									file.close()
									os.rename(localdir+OutputFilename,finaldir+OutputFilename)
									shutil.copyfile(finaldir+OutputFilename, backupdir+OutputFilename)
									time.sleep(0.5)
									log = open(logfile, "a")
									log.write(datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')+": arquivo "+OutputFilename+" baixado\n")
									log.close()
								except:
									print ("Error")
									print ('Closing file ' + filename)
									file.close()
									time.sleep(0.5)
	ftp.quit()
	cursor.close()

getpm('10.123.246.10','ossuser','Changeme_123','/opt/oss/server/var/fileint/pm/','10_')
