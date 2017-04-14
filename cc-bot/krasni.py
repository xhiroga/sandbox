from __future__ import absolute_import
import httplib
import urllib2, urllib
import urllib2, urllib, urlparse
import urllib2, urllib

import json

def main(params):
    btc_list={u"pair":u"XXBTZEUR,XXBTZUSD,XXBTZJPY"}

    kr = kraken()
    tk = kr.query_public(u"Ticker",btc_list)
    print u"this is ticker"
    print tk
    return {u"ticker":tk}


class kraken(object):

    def __init__(self, conn=None):
        self.uri = u'https://api.kraken.com'
        self.apiversion = u'0'
        self.conn = conn

    def _query(self, urlpath, req = {}, conn = None, headers = {}):
        url = self.uri + urlpath

        if conn is None:
            if self.conn is None:
                conn = Connection()
            else:
                conn = self.conn

        ret = conn._request(url, req, headers)
        # print(ret) # for polo test
        return json.loads(ret)


    def query_public(self, method, req = {}, conn = None):
        urlpath = u'/' + self.apiversion + u'/public/' + method
        return self._query(urlpath, req, conn)


class Connection(object):
    u"""Kraken.com connection handler.

    """

    def __init__(self, uri = u'api.kraken.com', timeout = 30):
        u""" Create an object for reusable connections.

        :param uri: URI to connect to.
        :type uri: str
        :param timeout: blocking operations' timeout (in seconds).
        :type timeout: int
        :returns: TODO
        :raises: TODO

        """
        __version__ = u'0.1.3'
        __url__ = u'https://github.com/veox/python3-krakenex'

        self.headers = {
            u'User-Agent': u'krakenex/' + __version__ +
            u' (+' + __url__ + u')'
        }
        self.conn = httplib.HTTPSConnection(uri, timeout = timeout)


    def close(self):
        u""" Close the connection.

        """
        self.conn.close()


    def _request(self, url, req = {}, headers = {}):
        u""" Send POST request to API server.

        :param url: fully-qualified URL with all necessary urlencoded
            information
        :type url: str
        :param req: additional API request parameters
        :type req: dict
        :param headers: additional HTTPS headers, such as API-Key and API-Sign
        :type headers: dict

        """
        data = urllib.urlencode(req)
        headers.update(self.headers)

        self.conn.request(u"POST", url, data, headers)
        response = self.conn.getresponse()

        return response.read().decode()
