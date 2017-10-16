#!/bin/bash

LOG="/home/etluser/log/auto-get-performance_40.log"
FTPLOG="/home/etluser/log/ftp-40.log"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

pgrep -f ftp-40
if [ $? -ne 0 ];then
   echo "$(horario): FTP executado.">>$LOG
   echo -e "-\n$(horario): Inicio da execucao.">>$FTPLOG
   python /etl/scripts/ftp-40.py
   python /etl/scripts/ftp-40_lte.py
   python /etl/scripts/ftp-40_gsm.py
   echo "$(horario): Fim da execucao.">>$FTPLOG
   exit 0
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0

