#!/bin/bash

LOG="/home/etluser/log/auto-get-performance_LTE.log"
FTPLOG="/home/etluser/log/ftp-10.log"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

pgrep -f ftp-10.py
if [ $? -ne 0 ];then
   echo "$(horario): FTP executado.">>$LOG
   echo -e "-\n$(horario): Inicio da execucao.">>$FTPLOG
   python /etl/scripts/ftp-10.py
   echo "$(horario): Fim da execucao.">>$FTPLOG
   exit 0
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0

