__author__ = 'Raquel'

from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from socket import error as SocketError

# <editor-fold desc="Protocol constants">
HTTP = 'http://'
preFTP = 'ftp://'
# </editor-fold>


def check_link(url):
    if url:
        try:
            urlopen(url, timeout=12)
        except HTTPError as e:
            return "{}: {}, {}".format(url, e.reason, e.code)
        except URLError as e:
            return "{}: {}".format(url, e.reason)
        except SocketError:
            return "{}: Socket Error".format(url)
        except ValueError:
            return "{}: Value Error".format(url)
    else:
        return "No link"
    return "working"