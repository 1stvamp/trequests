# encoding: utf-8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@license: Apache Licence
@file: proxy_demo.py
@time: 22/07/2017 12:04 PM

"""

import requests
import tornado.ioloop
import tornado.web
from tornalet import tornalet

from trequests import setup_session


class HttpFetcher:
    def __init__(self):
        self.session = requests.Session()
        # need to choose curl_httpclient
        setup_session(self.session, http_client="curl")
        # change to your proxy
        # self.proxies = {'http': 'http://username:password@host:port',
        #                 'https': 'https://username:password@host:port',
        #                 }
        self.proxies = {'http': 'http://:@127.0.0.1:11201',
                        'https': 'https://:@127.0.0.1:11201',
                        }

    def fetch(self, url):
        try:
            res = self.session.get(url, proxies=self.proxies)
            print res
        except Exception, e:
            print str(e)


class MainHandler(tornado.web.RequestHandler):
    @tornalet
    def get(self):
        print "start ..."
        hf = HttpFetcher()
        url = "http://www.google.com"  # some url need much time
        hf.fetch(url)
        print "end ..."


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
