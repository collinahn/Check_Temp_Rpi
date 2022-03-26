#!/bin/bash

TEMP_GPU=`/opt/vc/bin/vcgencmd measure_temp`
TEMP_GPU=${TEMP_GPU//temp=/}

echo ${TEMP_GPU}