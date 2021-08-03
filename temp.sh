#!/bin/bash

TEMP_CPU_RAW=`cat /sys/class/thermal/thermal_zone0/temp`
TEMP_CPU_INT=$((${TEMP_CPU_RAW}/1000))
TEMP_CPU_TEMP=$((${TEMP_CPU_RAW}/100))
TEMP_CPU_DECIMAL=$((${TEMP_CPU_TEMP} % ${TEMP_CPU_INT}))

TEMP_GPU=`/opt/vc/bin/vcgencmd measure_temp`
TEMP_GPU=${TEMP_GPU//temp=/}

echo $(date "+%Y-%m-%d %H:%M") Temperature CPU : ${TEMP_CPU_INT}"."${TEMP_CPU_DECIMAL}"'C, GPU : "${TEMP_GPU}

