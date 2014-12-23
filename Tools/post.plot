set term svg background "#FFFFFF"
set xlabel "Time in seconds"
set ylabel "Speed"
set grid
set title "FTP speed graph (three downloads)"
set output "Data/ftp-graph.svg"
plot "Data/ftp-post-curl.log" with linespoints 
set title "HTTP speed graph (three downloads)"
set output "Data/http-graph.svg"
plot "Data/http-post-curl.log" with linespoints 
