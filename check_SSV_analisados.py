import subprocess
import os
import telepot
import emoji
import csv
import sys
from datetime import datetime, time, timedelta

bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
WARNING = emoji.emojize(':warning_sign:')
OK = emoji.emojize(':heavy_check_mark:')
NOK = emoji.emojize(':thumbs_down_sign:')
user_id = sys.argv[1]

#today = str(datetime.now().strftime('%m/%d/%Y'))
today = str(datetime.now().date())

if datetime.now().time().hour < 3:
	yesterday = str(datetime.now().date() - timedelta(days=1))
else:
	yesterday = today
#today = str((datetime.now().date() - timedelta(days=1)).strftime('%m/%d/%Y'))
count = count_BA = count_CO = count_MG = count_NE = count_PR = count_ES = 0

with open('/etl/Controle_Antonio.csv', 'rt', encoding='utf-8') as file:
	reader = csv.reader(file, delimiter='\t')
	for row in reader :
		try:
			if row[5] == '23 - Aprovar SSV / PFRF'  and row[7] in (today, yesterday) and row[1] == 'CLARO BA/SE':
				count_BA += 1
			elif row[5] == '23 - Aprovar SSV / PFRF'  and row[7] in (today, yesterday) and row[1] == 'CLARO CO':
				count_CO += 1
			elif row[5] == '23 - Aprovar SSV / PFRF'  and row[7] in (today, yesterday) and row[1] == 'CLARO MG':
				count_MG += 1
			elif row[5] == '23 - Aprovar SSV / PFRF'  and row[7] in (today, yesterday) and row[1] == 'CLARO NE':
				count_NE += 1
			elif row[5] == '23 - Aprovar SSV / PFRF'  and row[7] in (today, yesterday) and row[1] == 'CLARO PR/SC':
				count_PR += 1
			elif row[5] == '23 - Aprovar SSV / PFRF'  and row[7] in (today, yesterday) and row[1] == 'CLARO RJ/ES':
				count_ES += 1
		except:
			pass

count = (count_BA + count_CO + count_MG + count_NE + count_PR + count_ES)

if count == 0:
	message = 'Nenhuma documentação analisada hoje.'
	bot.sendMessage(user_id, message + NOK)
else:
	message='\n'.join([item for item in (str(count_BA)+' BA',str(count_CO)+' CO',str(count_MG) +' MG',str(count_NE)+' NE',str(count_PR)+' PR/SC',str(count_ES)+' ES') if item[0] != '0'])
	bot.sendMessage(user_id, str(count)+' checked IR/SSVs today. '+OK+'\n\n'+message)
