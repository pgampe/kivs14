set term svg background "#FFFFFF"
set output "Data/ftp_graph.svg"
set title "FTP Speed Graph"
set timefmt "%s"
set xdata time
set xtics rotate
set ylabel "Speed"
set grid
plot "Data/ftp_speed.log" using 1:2 with lines
