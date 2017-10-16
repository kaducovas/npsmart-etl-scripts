#!/bin/bash

FTPDIR="/home/etluser/ftp_control/"
LOG="/home/etluser/log/check_ftp.log"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

cd $FTPDIR

for FILE in $(ls); do
	# How many seconds before file is deemed "older"
	OLDTIME=3600
	# Get current and file times
	CURTIME=$(date +%s)
	FILETIME=$(stat $FILE -c %Y)
	TIMEDIFF=$(expr $CURTIME - $FILETIME)

	# Check if file older
	if [ $TIMEDIFF -gt $OLDTIME ]; then
	   pkill -f -9 ${FILE%.*}
	   echo "$(horario): ${FILE%.*} killed" >> $LOG
	else
	   echo "$(horario): New ftp file $FILE ($TIMEDIFF seconds)" >> $LOG
	fi
done

exit 0
