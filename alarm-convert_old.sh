#!/bin/bash

#definições

IMP_DIR="/etl/common/alarm/temp/ftp"
OUT_DIR="/etl/common/alarm/temp/xslt"
TEMP_DIR="/etl/common/alarm/raw/"
XSLT="/etl/scripts/alarm.xsl"
SAXON="/usr/share/maven-repo/net/sf/saxon/Saxon-HE/debian/Saxon-HE-debian.jar"
TREADS=1
TestInterval=1
#LOG="/home/etluser/log/ConvertXml2Csv.log"


export TEMP_DIR OUT_DIR IMP_DIR XSLT SAXON LOG listaDeTabelas listaDeTabelas2 GLOBIGNORE

#mata a execução se o diretorio não for encontrado
[ -d $IMP_DIR ] || exit 1

#funcao que pega hora atual
horario()
{
  date +%d/%m/%Y" - "%H:%M:%S
}
#exporta a função para shells filhos
export -f horario

#função que faz a conversao
Convert2Csv () {

FileName=$1
#[ -r $FileName ] && xmllint --noout --valid ${IMP_DIR}/${FileName}

cd ${IMP_DIR}

#if [ $? -eq  0 ];then
        time  java -cp ${SAXON} net.sf.saxon.Transform -t -s:${FileName} -xsl:${XSLT} -o:${TEMP_DIR}/${FileName}.csv \
        && rm ${FileName}
		
		cd ${TEMP_DIR}
	    mv ${FileName}.csv ${OUT_DIR} 
		cd ${IMP_DIR}
}

#exporta a função para shells filhos
export -f Convert2Csv

#lista os arquivos ordenando por data e reverte a sequencia chamando a função a cada linha
TotalFiles=$(ls ${IMP_DIR}*.xml | wc -l)
cd ${IMP_DIR}
#echo -e "-\n$(horario): Inicio da execucao">>$LOG

parallel -j$TREADS -u Convert2Csv {}\;'echo -e "\nProgress: {#}/'$TotalFiles' Files converted\n"'\;sleep $TestInterval ::: $(ls *.xml)

#cd ${TEMP_DIR}/xslt
#rm -v *

#echo "$(horario): Fim da execucao">>$LOG

echo -e "\n"
exit 0


