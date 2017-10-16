#!/bin/bash

IMP_FILES='/home/etluser/npm/dumps/gexport/raw/'
EQUIPMENTS="LTE
BTS3900
NodeB"
TREADS=80%
TestInterval=0

export IMP_FILES TREADS TestInterval EQUIPMENTS

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}
export -f horario

for EQUIPMENT in $EQUIPMENTS; do
        case $EQUIPMENT in
		'NodeB' )
			VALUE='nodeb'
		;;
		'LTE')
			VALUE='enodeb'
		;;
		'BTS3900' )
			VALUE='sran'
		;;
		esac
        (TABLES=$(psql -d postgres -h 172.29.200.201 -U postgres -tc "SELECT distinct table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '${VALUE}_configuration' and table_name not in ('parameters') and table_name not like '%_history' order by table_name")
        for TABLE in $TABLES;do
		cd $IMP_FILES/$EQUIPMENT/$TABLE
		if [ "$(ls -A ./)" ]; then
			TotalFiles=$(ls *.csv | wc -l)
			pwd
			parallel -j$TREADS -u python3.4 /etl/scripts/fast_gexport.py $EQUIPMENT $VALUE $TABLE {}\;'echo -e "\nProgress: {#}/'$TotalFiles' Files parsed\n"'\;sleep $TestInterval ::: $(ls *.csv)
		fi
	done)&
done
wait
echo exit

exit 0
