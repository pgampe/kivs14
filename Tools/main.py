import urllib2
import re
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot

log = '../Data/PA.log'
log_url = 'rogue-01.informatik.uni-bonn.de/PA.log'
log_regex = '64 bytes from (\d*\.\d*\.\d*\.\d*): seq=(\d*) ttl=(\d*) time=(\d*\.\d*) ms'
log_graph = "../Data/pa_graph.svg"
log_boxplot = "../Data/pa_boxplot.svg"


def downloadFile(url='', filename=''):
    if url == '' or filename == '':
        return
    d = getFile(url, ftp=False)
    f = open(filename, 'w')
    f.write(d)
    d.close()
    f.close()


def getFile(url='', ftp=True, asObject=False):
    """
    Fetches the most recent data from the server. Throws URLError if
    the server is offline or the file can't be found.

    :param url: The URL without a scheme.
    :param ftp: True if FTP, False if HTTP.
    :param asObject: If True, this method returns an iterable Object.

    :returns: The recent data as String or Object.
    """
    if ftp:
        response = urllib2.urlopen('ftp://' + url)
    else:
        response = urllib2.urlopen('http://' + url)
    if asObject:
        return response
    result = response.read()
    response.close()
    return result


def analizeLogFile(f):
    """
    :param f: The logfile file object
    :return: The set data with all data points below each timestamp or False on error

    :type f: file
    """
    data = {}
    line = f.readline()
    regex = re.compile(log_regex)

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


def plot_log(d):
    sorted(d)
    timestamps = []
    rtt_min = []
    rtt_avg = []
    rtt_max = []
    for i in d:
        timestamps.append(i)
        rtt = []
        for data in d[i]:
            rtt.append(float(data[3]))
        rtt_min.append(np.min(rtt))
        rtt_max.append(np.max(rtt))
        rtt_avg.append(np.mean(rtt))
    plt.plot(timestamps, rtt_max, 'r,')
    plt.plot(timestamps, rtt_min, 'g,')
    plt.plot(timestamps, rtt_avg, 'b,')
    plt.xlabel('Timestamp')
    plt.ylabel('Time in ms')
    plt.savefig(log_graph, format='svg', frameon=True)

def boxplot_segmented_data(minTTL, step, segData):
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


        #data.append()
        #plt.boxplot(segData[int(x)])
        curTTL = curTTL + step
    plt.boxplot(allData, labels=allTTL)
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
        #print(inputData[i][0][2] + " comes in "+str(seg))

        segments[seg][inputData[i][0][0]] = (inputData[i])
    return minTTL, step, segments


def main():
    if not os.path.isfile(log):
        downloadFile(log_url)
    f = file(log, 'r')
    r = analizeLogFile(f)
    if r == False:
        f.close()
        print 'Failed to parse file.'
        return 1
    '''
        r:
        {Timestamp: (IP, seq, ttl, time), Timestamp: ...}
    '''


    minTTL, step, TTLData = segment_data(r)
    boxplot_segmented_data(minTTL, step, TTLData)
    plot_log(r)

    f.close()
    return 0

main()