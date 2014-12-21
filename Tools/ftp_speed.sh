#!/bin/bash
echo $(date "+%s") $(curl -o /dev/null -r0-1048576 -s -w "%{speed_download}" "ftp://rogue-01.informatik.uni-bonn.de/PA.log") >> Data/ftp_speed.log
sleep 10
echo $(date "+%s") $(curl -o /dev/null -r0-1048576 -s -w "%{speed_download}" "ftp://rogue-01.informatik.uni-bonn.de/PA.log") >> Data/ftp_speed.log
sleep 10
echo $(date "+%s") $(curl -o /dev/null -r0-1048576 -s -w "%{speed_download}" "ftp://rogue-01.informatik.uni-bonn.de/PA.log") >> Data/ftp_speed.log
