#!/bin/bash

cd $(dirname $0)"/.."

URL='http://rogue-01.informatik.uni-bonn.de/linux-3.9.2.tar.xz'
# Download the file, redirect progress bar to stdout
# replace carriage return with newline
# filter unwanted lines (head, empty and invalid data)
# replace multiple spaces with tabs
# append this to log file  (and print to term)
curl -L -o /dev/null "$URL" 2>&1 |tr '\r' '\n' >> "Data/http-curl.log"
#grep -v 'Total'| grep -v '^$'| grep -v "\--:--:--" |tr -s " " "\t" |tee -a "Data/http-curl.log"
# and now with ftp
URL='ftp://rogue-01.informatik.uni-bonn.de/linux-3.9.2.tar.xz'
curl -L -o /dev/null "$URL" 2>&1 |tr '\r' '\n' >> "Data/ftp-curl.log"
# select the 11st and 13th column, replace 
#cat "Data/http-curl.log" |cut -f11,13 
