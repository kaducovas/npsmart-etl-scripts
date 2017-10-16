#!/bin/bash

LOG="/home/etluser/log/autoParse_LTE.log"
PARSELOG="/home/etluser/log/parsePM-LTE.log"
IMP_FILES="/etl/lte/performance/converted/"
TREADS=50%
TestInterval=0

export IMP_FILES LOG PARSELOG TREADS TestInterval

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}
export -f horario

if [[ ! $(ls -A $IMP_FILES/*.csv) ]];then
   echo "$(horario): Nao ha arquivos a serem carregados.">>$LOG
   exit 1
else
   pgrep -f parseLTE_novo.py
   if [ $? -ne 0 ];then
      echo "$(horario): FTP executado.">>$LOG
      echo -e "-\n$(horario): Inicio da execucao.">>$PARSELOG
	  cd $IMP_FILES
	  TotalFiles=$(ls *.csv | wc -l)  
      parallel -j$TREADS -u python3.4 /etl/scripts/parseLTE_novo.py {}\;'echo -e "\nProgress: {#}/'$TotalFiles' Files parsed\n"'\;sleep $TestInterval ::: $(ls *.csv | sort -t "_" -k 5)
      echo "$(horario): Fim da execucao.">>$PARSELOG
      exit 0
   fi
fi

echo "$(horario): Processo ja em execucao.">>$LOG
exit 0

