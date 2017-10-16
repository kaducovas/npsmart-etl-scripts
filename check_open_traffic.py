import subprocess
import os
import telepot
import emoji
import csv
import sys

bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
WARNING = emoji.emojize(':warning_sign:')
OK = emoji.emojize(':thumbs_up_sign:')
CHECK = emoji.emojize(':white_heavy_check_mark:')
user_id = sys.argv[1]

message_BA = ''
message_CO = ''
message_MG = ''
message_NE = ''
message_PR = ''
message_ES = ''

count = count_BA = count_CO = count_MG = count_NE = count_PR = count_ES = 0
with open('/etl/Controle_Antonio.csv', 'rt', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader :
	    try:
	      if row[5].startswith(('22', '26')) and row[15] in ['P','p'] and row[1] == 'CLARO BA/SE':
	          message_BA = message_BA+'\n'+row[0]+': '+row[9]+'\n'
	          count_BA += 1

	      elif row[5].startswith(('22', '26')) and row[15] in ['P','p'] and row[1] == 'CLARO CO':
	          message_CO = message_CO+'\n'+row[0]+': '+row[9]+'\n'
	          count_CO += 1

	      elif row[5].startswith(('22', '26')) and row[15] in ['P','p'] and row[1] == 'CLARO MG':
	          message_MG = message_MG+'\n'+row[0]+': '+row[9]+'\n'
	          count_MG += 1

	      elif row[5].startswith(('22', '26')) and row[15] in ['P','p'] and row[1] == 'CLARO NE':
	          message_NE = message_NE+'\n'+row[0]+': '+row[9]+'\n'
	          count_NE += 1

	      elif row[5].startswith(('22', '26')) and row[15] in ['P','p'] and row[1] == 'CLARO PR/SC':
	          message_PR = message_PR+'\n'+row[0]+': '+row[9]+'\n'
	          count_PR += 1

	      elif row[5].startswith(('22', '26')) and row[15] in ['P','p'] and row[1] == 'CLARO RJ/ES':
	          message_ES = message_ES+'\n'+row[0]+': '+row[9]+'\n'
	          count_ES += 1
	    except:
	       print (row)
	       pass

if message_BA:
	if count_BA == 1:
		message = str(count_BA) + ' pendecy in BA:\n'+message_BA
	else:
		message = str(count_BA) + ' pendencies in BA:\n'+message_BA
	bot.sendMessage(user_id, message)
if message_CO:
	if count_CO == 1:
		message = str(count_CO) + ' pendecy in CO:\n'+message_CO
	else:
		message = str(count_CO) + ' pendencies in CO:\n'+message_CO
	bot.sendMessage(user_id, message)
if message_MG:
	if count_MG == 1:
		message = str(count_MG) + ' pendecy in MG:\n'+message_MG
	else:
		message = str(count_MG) + ' pendencies in MG:\n'+message_MG
	bot.sendMessage(user_id, message)
if message_NE:
	if count_NE == 1:
		message = str(count_NE) + ' pendecy in NE:\n'+message_NE
	else:
		message = str(count_NE) + ' pendencies in NE:\n'+message_NE
	bot.sendMessage(user_id, message)
if message_PR:
	if count_PR == 1:
		message = str(count_PR) + ' pendecy in PR/SC:\n'+message_PR
	else:
		message = str(count_PR) + ' pendencies in PR/SC:\n'+message_PR
	bot.sendMessage(user_id, message)
if message_ES:
	if count_ES == 1:
		message = str(count_ES) + ' pendecy in ES:\n'+message_ES
	else:
		message = str(count_ES) + ' pendencies in ES:\n'+message_ES
	bot.sendMessage(user_id, message)

count = (count_BA + count_CO + count_MG + count_NE + count_PR + count_ES)

if count == 0:
	message = 'None pendency on Step 26. '+OK
elif count == 1:
	message = 'One pendecy on step 26'+WARNING
else:
	message = 'Total of '+str(count)+' pendencies on step 26'+WARNING
	
secondmessage = ''
for region, count in [['BA',count_BA],['CO',count_CO],['MG',count_MG],['NE',count_NE],['PR',count_PR],['ES',count_ES]]:
	if not count:
		secondmessage = secondmessage + '\n' + region + ': ' + CHECK
	else:
		secondmessage = secondmessage + '\n' + region + ': ' + str(count).zfill(2)

#secondmessage='\n'.join([item for item in (str(count_BA)+' BA',str(count_CO)+' CO',str(count_MG) +' MG',str(count_NE)+' NE',str(count_PR)+' PR/SC',str(count_ES)+' ES') if item[0] != '0'])
bot.sendMessage(user_id, message+'\n'+secondmessage)
