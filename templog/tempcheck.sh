#!/bin/bash

if [ ! -d /home/pi/templog ] ; then
	mkdir /home/pi/templog
fi

while [ true ]
do
	/home/pi/temp.sh >> /home/pi/templog/tempcheck.log
	sleep 10m
done
