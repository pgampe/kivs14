#!/bin/bash
exit
cd $(dirname $0)"/.."
echo $$ > speed.pid

while true; do sleep 5; t=$(date "+%s"); bash Tools/http_speed.sh $t \&; done &
while true; do sleep 5; s=$(date "+%s"); bash Tools/ftp_speed.sh $s \&; done &

rm speed.pid
