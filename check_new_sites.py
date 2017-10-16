import telepot
import emoji
import csv
import sys

bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
WARNING = emoji.emojize(':warning_sign:')
JOINHA = emoji.emojize(':thumbs_up_sign:')
CHECK = emoji.emojize(':white_heavy_check_mark:')
user_id = sys.argv[1]

message_BA_23 = ''
message_CO_23 = ''
message_MG_23 = ''
message_NE_23 = ''
message_PR_23 = ''
message_ES_23 = ''

count_23 = count_BA_23 = count_CO_23 = count_MG_23 = count_NE_23 = count_PR_23 = count_ES_23 = 0

message_BA_26 = ''
message_CO_26 = ''
message_MG_26 = ''
message_NE_26 = ''
message_PR_26 = ''
message_ES_26 = ''

message_23 = ''
message_26 = ''

count_26 = count_BA_26 = count_CO_26 = count_MG_26 = count_NE_26 = count_PR_26 = count_ES_26 = 0

with open('/etl/Controle_Antonio.csv', 'rt', encoding='utf-8') as csvfile1:
	with open ('/etl/huaweiStatusReport.csv','r', newline="\n", encoding="utf-8") as csvfile2:
		reader1 = csv.reader(csvfile1, delimiter='\t')
		reader2 = csv.reader(csvfile2, delimiter=';')
		rows1_col_a = [row[0] for row in reader1 if row[5].startswith('26')]
		rows2 = [row for row in reader2]        
		for row in rows2:
			if row[5] == '23 - Aprovar SSV / PFRF':
				if row[1] == 'CLARO BA/SE':
					count_BA_23 += 1
					message_BA_23 = message_BA_23+'\n'+row[0]
				elif row[1] == 'CLARO CO':
					count_CO_23 += 1
					message_CO_23 = message_CO_23+'\n'+row[0]
				elif row[1] == 'CLARO MG':
					count_MG_23 += 1
					message_MG_23 = message_MG_23+'\n'+row[0]
				elif row[1] == 'CLARO NE':
					count_NE_23 += 1
					message_NE_23 = message_NE_23+'\n'+row[0]
				elif row[1] == 'CLARO PR/SC':
					count_PR_23 += 1
					message_PR_23 = message_PR_23+'\n'+row[0]
				elif row[1] == 'CLARO RJ/ES':
					count_ES_23 += 1
					message_ES_23 = message_ES_23+'\n'+row[0]
			else:
				if row[0] not in rows1_col_a:
					if row[1] == 'CLARO BA/SE':
						count_BA_26 += 1
						message_BA_26 = message_BA_26+'\n'+row[0]
					elif row[1] == 'CLARO CO':
						count_CO_26 += 1
						message_CO_26 = message_CO_26+'\n'+row[0]
					elif row[1] == 'CLARO MG':
						count_MG_26 += 1
						message_MG_26 = message_MG_26+'\n'+row[0]
					elif row[1] == 'CLARO NE':
						count_NE_26 += 1
						message_NE_26 = message_NE_26+'\n'+row[0]
					elif row[1] == 'CLARO PR/SC':
						count_PR_26 += 1
						message_PR_26 = message_PR_26+'\n'+row[0]
					elif row[1] == 'CLARO RJ/ES':
						count_ES_26 += 1
						message_ES_26 = message_ES_26+'\n'+row[0]
						
count_23 = (count_BA_23 + count_CO_23 + count_MG_23 + count_NE_23 + count_PR_23 + count_ES_23)
count_26 = (count_BA_26 + count_CO_26 + count_MG_26 + count_NE_26 + count_PR_26 + count_ES_26)

if count_23 == 0 and count_26 == 0:
	bot.sendMessage(user_id, 'Zero new site' + JOINHA)

if count_23:
	for region,count,message in [['BA',count_BA_23,message_BA_23],['CO',count_CO_23,message_CO_23],['MG',count_MG_23,message_MG_23],['NE',count_NE_23,message_NE_23],['PR/SC',count_PR_23,message_PR_23],['ES',count_ES_23,message_ES_23]]:
		if message:
			message_23 = message_23+str(count)+' '+region+':'+message+'\n\n'
	if count_23 == 1:
		bot.sendMessage(user_id, str(count_23)+' new site on step 23 '+WARNING+'\n\n'+message_23)
	else:
		bot.sendMessage(user_id, str(count_23)+' new sites on step 23 '+WARNING+'\n\n'+message_23)

message = ''
for region, count in [['BA',count_BA_23],['CO',count_CO_23],['MG',count_MG_23],['NE',count_NE_23],['PR',count_PR_23],['ES',count_ES_23]]:
	if not count:
		message = message + '\n' + region + ': ' + CHECK
	else:
		message = message + '\n' + region + ': ' + str(count).zfill(2)
message = 'Step 23 Backlog:\n' + message
#message = 'Step 23 Backlog:\nBA: '+str(count_BA_23).zfill(2)+'\nCO: '+str(count_CO_23).zfill(2)+'\nMG: '+str(count_MG_23).zfill(2)+'\nNE: '+str(count_NE_23).zfill(2)+'\nPR: '+str(count_PR_23).zfill(2)+'\nES: '+str(count_ES_23).zfill(2)
bot.sendMessage(user_id, message)

if count_26:
	for region,count,message in [['BA',count_BA_26,message_BA_26],['CO',count_CO_26,message_CO_26],['MG',count_MG_26,message_MG_26],['NE',count_NE_26,message_NE_26],['PR/SC',count_PR_26,message_PR_26],['ES',count_ES_26,message_ES_26]]:
		if message:
			message_26 = message_26+str(count)+' '+region+':'+message+'\n\n'
	if count_26 == 1:
		bot.sendMessage(user_id, str(count_26)+' new site on step 26 '+WARNING+'\n\n'+message_26)
	else:
		bot.sendMessage(user_id, str(count_26)+' new sites on step 26 '+WARNING+'\n\n'+message_26)
message = ''
for region, count in [['BA',count_BA_26],['CO',count_CO_26],['MG',count_MG_26],['NE',count_NE_26],['PR',count_PR_26],['ES',count_ES_26]]:
	if not count:
		message = message + '\n' + region + ': ' + CHECK
	else:
		message = message + '\n' + region + ': ' + str(count).zfill(2)
message = 'Step 26 Backlog:\n' + message
#message = 'Step 26 Backlog:\nBA: '+str(count_BA_26).zfill(2)+'\nCO: '+str(count_CO_26).zfill(2)+'\nMG: '+str(count_MG_26).zfill(2)+'\nNE: '+str(count_NE_26).zfill(2)+'\nPR: '+str(count_PR_26).zfill(2)+'\nES: '+str(count_ES_26).zfill(2)
bot.sendMessage(user_id, message)