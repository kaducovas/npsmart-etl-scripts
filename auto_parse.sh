#!/bin/bash

IMP_FILES="/etl/umts/performance/converted/"
LOG="/home/etluser/log/auto_parse.log"
PARSELOG="/home/etluser/log/parsePM.log"
TREADS=25%
TestInterval=0

export IMP_FILES LOG PARSELOG TREADS TestInterval

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}
export -f horario

if [[ ! $(ls -A $IMP_FILES) ]];then
   echo "$(horario): Nao ha arquivos a serem carregados.">>$LOG
   exit 1
else
   #ps ax | grep parsePM.py
   pgrep -f parseMain.py
   if [ $? -ne 0 ];then
      echo "$(horario): Parse executado.">>$LOG
      echo -e "-\n$(horario): Inicio da execucao.">>$PARSELOG
      cd $IMP_FILES
	  TotalFiles=$(ls *.csv | wc -l)  
	  parallel -j$TREADS -u python3.4 /etl/scripts/parseMain.py {}\;'echo -e "\nProgress: {#}/'$TotalFiles' Files parsed\n"'\;sleep $TestInterval ::: $(ls *.csv | sort -t "_" -k 5)
      echo "$(horario): Fim da execucao.">>$PARSELOG
      exit 0
   fi
fi

echo "$(horario): Processo ja em execucao.">>$LOG

exit 0

