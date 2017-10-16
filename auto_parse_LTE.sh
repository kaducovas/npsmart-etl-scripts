#!/bin/bash

LOG="/home/etluser/log/autoParse_LTE.log"
PARSELOG="/home/etluser/log/parsePM-LTE.log"
IMP_FILES="/etl/lte/performance/converted/"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

if [[ ! $(ls -A $IMP_FILES/*.csv) ]];then
   echo "$(horario): Nao ha arquivos a serem carregados.">>$LOG
   exit 1
else
   pgrep -f parseLTE.py
   if [ $? -ne 0 ];then
      echo "$(horario): FTP executado.">>$LOG
      echo -e "-\n$(horario): Inicio da execucao.">>$PARSELOG
      python3.4 /etl/scripts/parseLTE.py
      echo "$(horario): Fim da execucao.">>$PARSELOG
      exit 0
   fi
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0

