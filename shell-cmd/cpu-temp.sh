#!/bin/bash

TEMP_CPU_RAW=`cat /sys/class/thermal/thermal_zone0/temp`
TEMP_CPU_INT=$((${TEMP_CPU_RAW}/1000))
TEMP_CPU_DECIMAL=$(($((${TEMP_CPU_RAW}%1000))/100))

echo ${TEMP_CPU_INT}"."${TEMP_CPU_DECIMAL}"'C"