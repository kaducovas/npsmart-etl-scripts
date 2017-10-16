#!/bin/bash

LOG="/home/etluser/log/auto-get-performance_ATAE2.log"
FTPLOG="/home/etluser/log/ftp-atae2.log"
FTPDIR="/home/etluser/ftp_control/"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

pgrep -f ftp-2atae
if [ $? -ne 0 ];then
   echo "$(horario): FTP executado.">>$LOG
   echo -e "-\n$(horario): Inicio da execucao.">>$FTPLOG
   echo "$(horario): ftp-2atae execucao.">> $FTPDIR/ftp-2atae.txt
   python3.4 /etl/scripts/ftp-2atae.py
   rm -f $FTPDIR/ftp-2atae.txt && echo "$(horario): ftp-2atae_lte execucao.">> $FTPDIR/ftp-2atae_lte.txt
   python3.4 /etl/scripts/ftp-2atae_lte.py
   rm -f $FTPDIR/ftp-2atae_lte.txt && echo "$(horario): ftp-2atae_gsm execucao.">> $FTPDIR/ftp-2atae_gsm.txt
   python3.4 /etl/scripts/ftp-2atae_gsm.py
   rm -f $FTPDIR/ftp-2atae_gsm.txt
   echo "$(horario): Fim da execucao.">>$FTPLOG
   exit 0
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0

