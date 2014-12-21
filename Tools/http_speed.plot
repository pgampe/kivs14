set term svg background "#FFFFFF"
set output "Data/http_graph.svg"
set title "HTTP Speed Graph"
set timefmt "%s"
set xdata time
set xtics rotate
set ylabel "Speed"
set grid
plot "Data/http_speed.log" using 1:2 with lines
