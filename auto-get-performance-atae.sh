#!/bin/bash

LOG="/home/etluser/log/auto-get-performance_ATAE.log"
FTPLOG="/home/etluser/log/ftp-atae.log"
FTPDIR="/home/etluser/ftp_control/"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

pgrep -f ftp-atae
if [ $? -ne 0 ];then
   echo "$(horario): FTP executado.">>$LOG
   echo -e "-\n$(horario): Inicio da execucao.">>$FTPLOG
   echo "$(horario): ftp-atae execucao.">> $FTPDIR/ftp-atae.txt
   python /etl/scripts/ftp-atae.py
   rm -f $FTPDIR/ftp-atae.txt && echo "$(horario): ftp-atae_lte execucao.">>$FTPDIR/ftp-atae_lte.txt
   python /etl/scripts/ftp-atae_lte.py
   rm -f $FTPDIR/ftp-atae_lte.txt && echo "$(horario): ftp-atae_gsm execucao.">>$FTPDIR/ftp-atae_gsm.txt
   python /etl/scripts/ftp-atae_gsm.py
   rm -f $FTPDIR/ftp-atae_gsm.txt
   echo "$(horario): Fim da execucao.">>$FTPLOG
   exit 0
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0

