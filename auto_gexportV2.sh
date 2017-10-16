#!/bin/bash

IMP_FILES='/home/etluser/npm/dumps/gexport/raw/'
EQUIPMENTS="LTE
BTS3900
NodeB"
TREADS=60%
TestInterval=0

export IMP_FILES TREADS TestInterval EQUIPMENTS

horario()
{
date +%d/%m/%Y" - "%H:%M:%S
}
export -f horario

parseGexport()
{
	EQUIPMENT=$1
	VALUE=$2
	TABLE=$3
	if [ "$(ls -A $IMP_FILES/$EQUIPMENT/$TABLE)" ]; then
	cd $IMP_FILES/$EQUIPMENT/$TABLE
		pwd
		for FILE in $(ls); do
			python3.4 /etl/scripts/fast_gexport.py $EQUIPMENT $VALUE $TABLE $FILE
		done
	fi
}
export -f parseGexport

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
        TABLES=$(psql -d postgres -h 172.29.200.201 -U postgres -tc "SELECT distinct table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '${VALUE}_configuration' and table_name not in ('parameters') and table_name not like '%_history' order by table_name")
   	TotalTables=$(echo $TABLES | wc -w)
	parallel -j$TREADS -u parseGexport $EQUIPMENT $VALUE {} \;'echo -e "\nProgress: {#}/'$TotalTables' Tables parsed\n"'\;sleep $TestInterval ::: $TABLES
	
done

exit 0
