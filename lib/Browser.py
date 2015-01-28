import httplib
import urllib2
import socket
import urllib

socket.setdefaulttimeout(10)


class Browser:
    def __init__(self):
        pass

    def fetch(self, url, data=None):
        req = urllib2.Request(url, urllib.urlencode(data))
        response = urllib2.urlopen(req)
        return response.read()