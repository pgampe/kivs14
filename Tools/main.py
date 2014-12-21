import urllib2
import re
import os.path
import numpy as np
import matplotlib.pyplot as plt

log = '../Data/PA.log'
log_url = 'rogue-01.informatik.uni-bonn.de/PA.log'
log_regex = '64 bytes from (\d*\.\d*\.\d*\.\d*): seq=(\d*) ttl=(\d*) time=(\d*\.\d*) ms'
log_graph = "../Data/pa_graph.svg"


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


def main():
    if not os.path.isfile(log):
        downloadFile(log_url)
    f = file(log, 'r')
    r = analizeLogFile(f)
    if r == False:
        f.close()
        print 'Failed to parse file.'
        return 1

    plot_log(r)

    f.close()
    return 0

main()