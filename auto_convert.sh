#!/bin/bash

IMP_FILES="/etl/umts/performance/raw/"
LOG="/home/etluser/log/auto_convert.log"

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}

if [[ ! $(ls -A $IMP_FILES/*.xml $IMP_FILES/*.tmp) ]];then
   echo "$(horario): Nao ha arquivos a serem carregados.">>$LOG
   exit 1
else
   pgrep -f pm-convert.sh
   if [ $? -ne 0 ];then
      echo "$(horario): Converted executado.">>$LOG
      /etl/scripts/pm-convert.sh
      exit 0
   fi
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0
