#!/bin/bash

cd $(dirname $0)"/.."

# filter unwanted lines (head, empty and invalid data)
# replace multiple spaces with tabs
# select column 13 (the speed)
cat "Data/http-curl.log" |grep -v 'Total'| grep -v '^$'| grep -v "\--:--:--" |tr -s " " "\t" |cut -f13 |awk '/[0-9]$/{print $1;next};/[mM]$/{printf "%u\n", $1*(1024*1024);next};/[kK]$/{printf "%u\n", $1*1024;next}' > "Data/http-post-curl.log"
# and now with ftp
cat "Data/ftp-curl.log" |grep -v 'Total'| grep -v '^$'| grep -v "\--:--:--" |tr -s " " "\t" |cut -f13 |awk '/[0-9]$/{print $1;next};/[mM]$/{printf "%u\n", $1*(1024*1024);next};/[kK]$/{printf "%u\n", $1*1024;next}' > "Data/ftp-post-curl.log"

# now run through gnuplot
gnuplot Tools/post.plot
