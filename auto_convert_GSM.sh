#!/bin/bash

IMP_FILES="/etl/gsm/performance/raw/"
LOG="/home/etluser/log/auto_convert_GSM.log"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

if [[ ! $(ls -A $IMP_FILES/*.xml) ]];then
   echo "$(horario): Nao ha arquivos a serem carregados.">>$LOG
   exit 1
else
   pgrep -f GSM_pmConvert.sh
   if [ $? -ne 0 ];then
      echo "$(horario): Converted executado.">>$LOG
      /etl/scripts/GSM_pmConvert.sh
      exit 0
   fi
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0

