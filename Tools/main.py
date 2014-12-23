import urllib2
import re
import os.path
import numpy as np
import matplotlib.pyplot as plt
import argparse


def downloadFile(url='', filename=''):
    """
    Downloads a file from a server and saves it into a local file

    :param url: The URL to download
    :param filename: The filename to save the downloaded data to
    :return: void
    """
    if url == '' or filename == '':
        return
    d = urllib2.urlopen(url)
    f = open(filename, 'w')
    f.write(d.read())
    d.close()
    f.close()


def analizeLogFile(f, start, end):
    """
    :param f: The logfile file object
    :param start: The start time
    :param end: The end time
    :return: The set data with all data points below each timestamp or False on error

    :type f: file
    """
    data = {}
    line = f.readline()
    regex = re.compile('64 bytes from (\d*\.\d*\.\d*\.\d*): seq=(\d*) ttl=(\d*) time=(\d*\.\d*) ms')

    # iterate file until EOF
    while True:
        # each time we start with the timestamp
        try:
            timestamp = int(line)
        except ValueError:
            timestamp = 0
        if timestamp == 0:
            if f.readline() == '':
                return data
            else:
                return False

        # next line must start with PING
        line = f.readline()
        if line[:4] == 'PING':
            line = f.readline()
        else:
            continue

        # now comes our data set (max 10 pings)
        currentSet = []
        for i in range(0, 10):
            line = f.readline()
            if line[:2] != '64':
                break
            r = regex.match(line)
            currentSet.append(r.groups())
        if start < timestamp < end:
            data[timestamp] = currentSet

        # empty line after data block
        if line != '\n':
            continue

        # statistics block with three lines in total (ignored)
        line = f.readline()
        if line[:3] == '---':
            f.readline()
            f.readline()
        else:
            continue

        # read the line for next run of the loop
        line = f.readline()

    return False


def plot_log(data, log_graph):
    """
    Plot the graph for all data points
    :param data: The log data
    :param log_graph: The file to save the SVG image
    :return:
    """
    sorted(data)
    timestamps = []
    rtt_min = []
    rtt_avg = []
    rtt_max = []
    for i in data:
        timestamps.append(i)
        rtt = []
        for values in data[i]:
            rtt.append(float(values[3]))
        rtt_min.append(np.min(rtt))
        rtt_max.append(np.max(rtt))
        rtt_avg.append(np.mean(rtt))
    plt.plot(timestamps, rtt_max, 'r,', label='RTT max')
    plt.plot(timestamps, rtt_min, 'g,', label='RTT min')
    plt.plot(timestamps, rtt_avg, 'b,', label='RTT avg')
    plt.xlabel('Timestamp')
    plt.ylabel('Time in ms')
    plt.legend()
    plt.savefig(log_graph, format='svg', frameon=True)
    plt.close()


def boxplot_segmented_data(minTTL, step, segData, log_boxplot):
    """
    Plots the already segmented data.
    :param minTTL: The minimum TTL
    :param step: The step between each plot
    :param segData: The segmented data
    :param log_boxplot: The file to save the SVG image
    :return:
    """
    curTTL = minTTL
    allData = []
    allTTL = []
    for x in segData:
        data = []
        for y in x:
            for z in x[y]:
                data.append(float(z[3]))
        # Pick desired data
        if not data:
            # no data here. continue
            curTTL = curTTL + step
            continue
        allData.append(data)
        allTTL.append(int(curTTL))
        curTTL = curTTL + step
    plt.boxplot(allData)
    plt.xlabel("TTL [Hop]")
    plt.ylabel("Time [ms]")
    plt.savefig(log_boxplot, format='svg', frameon=True)
    plt.close()


def segment_data(inputData):
    '''
    Segments data after TTL. Output is guaranteed to be less or equal to 20 entries.
    Entry might be empty!!
    :param inputData:
    :return: minTTL, maxTTL, segmentedData
    '''
    minTTL = float("inf") # Infinity, for first check
    maxTTL = -1
    for i in inputData:
        if minTTL > float(inputData[i][0][2]): # Check for smaller TTL
            minTTL = float(inputData[i][0][2])
        if maxTTL < float(inputData[i][0][2]): # Check for bigger TTL
            maxTTL = float(inputData[i][0][2])
    # In reality: 43.0 minTTL
    # In reality: 56.0 maxTTL
    if minTTL == float("inf") or maxTTL == -1:
        return False # Wut?
    # Make Segments... for each TTL one. Except when more than say... 20. Then just make 20.
    if maxTTL == minTTL:
        return False # I don't want to work with these data.
    if maxTTL - minTTL <= 20:
        step = 1
        max = int(maxTTL-minTTL+0.5)
    else:
        step = (maxTTL-minTTL)/20 # Meh... cheap solution, but it works. Keep in mind that TTL are natural numbers
        max = 20
    segments = []
    for x in range(0, max+1, step):
        segments.insert(x, {})
    for i in inputData:
        seg = int((float(inputData[i][0][2])-minTTL) * step + 0.5) # int(x +0.5) rounds x to nearest integer
        segments[seg][inputData[i][0][0]] = (inputData[i])
    return minTTL, step, segments


def main():
    parser = argparse.ArgumentParser(description='Analyze data from PING measurement.')
    parser.add_argument('--start', default=0, type=int, help='The start time for the plots. Default: %(default)s')
    parser.add_argument('--end', default=2147483647, type=int, help='The end time for the plots. Default: %(default)s')
    parser.add_argument('--log-url', default='ftp://rogue-01.informatik.uni-bonn.de/PA.log', help='The URL do download. Default: %(default)s')
    parser.add_argument('--log-file', default='../Data/PA.log', help='The file to save the log file contents. Default: %(default)s')
    parser.add_argument('--log-graph', default='../Data/pa_graph.svg', help='The file to save the generated linegraph SVG image. Default: %(default)s')
    parser.add_argument('--log-boxplot', default='../Data/pa_boxplot.svg', help='The file to save the generated boxplot SVG image. Default: %(default)s')
    args = parser.parse_args()

    if not os.path.isfile(args.log_file):
        downloadFile(args.log_url)
    f = file(args.log_file, 'r')
    r = analizeLogFile(f, args.start, args.end)
    f.close()
    if r == False:
        print 'Failed to parse file.'
        return 1
    '''
        r:
        {Timestamp: (IP, seq, ttl, time), Timestamp: ...}
    '''

    plot_log(r, args.log_graph)
    minTTL, step, TTLData = segment_data(r)
    boxplot_segmented_data(minTTL, step, TTLData, args.log_boxplot)

    return 0

main()