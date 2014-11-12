import urllib2

def getRecentData(useFtp = True, asObject = False):
    """Fetches the most recent data from the server. Throws URLError if
    the server is offline or the file can't be found.
    \param useFTP True if FTP, False if HTTP.
    \param asObject If True, this method returns an iterable Object.
    If False it returns a String. Keep in mind that you have to close() the
    Object after you're done.
    \returns The recent data as String or Object."""
    if useFtp:
        response = urllib2.urlopen('ftp://rogue-01.informatik.uni-bonn.de/PA.log')
    else:
        response = urllib2.urlopen('http://rogue-01.informatik.uni-bonn.de/PA.log')
    if asObject:
        return response
    result = response.read()
    response.close()
    return result

yourData = getRecentData(asObject=True)

for line in yourData:
    print(line) # Double linebreaks, because \r\n in file + print()-Linebreak.
yourData.close()