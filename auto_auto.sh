#!/bin/bash

while [ 1 ]
do
/etl/scripts/auto-get-performance-15.sh;/etl/scripts/auto-get-performance-40.sh;/etl/scripts/auto-get-performance-atae.sh;/etl/scripts/auto-get-performance-10.sh;/etl/scripts/auto_convert.sh;/etl/scripts/auto_parse.sh;/etl/scripts/auto_convert_LTE.sh;/etl/scripts/auto_parse_LTE.sh;/etl/scripts/auto_convert_GSM.sh;/etl/scripts/auto_parse_GSM.sh
sleep 600
done