#!/bin/bash
t=$1
echo $t $(curl -o /dev/null -r0-1048576 -s -w "%{speed_download}" "ftp://rogue-01.informatik.uni-bonn.de/PA.log") >> Data/ftp_speed.log
