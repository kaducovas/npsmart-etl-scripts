#!/bin/bash

LOCAL_SCRIPTS="/etl/scripts/"

sleep 1


#time ${LOCAL_SCRIPTS}./get-eam.sh
time ${LOCAL_SCRIPTS}./eam-convert.sh


exit 0

