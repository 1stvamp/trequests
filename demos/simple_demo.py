# encoding: utf-8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@license: Apache Licence
@file: simple_demo.py
@time: 22/07/2017 11:06 AM

"""
import requests
import tornado.ioloop
import tornado.web
from tornalet import tornalet
from trequests import setup_session


class HttpFetcher:
    def __init__(self):
        self.session = requests.Session()
        # this will add AsyncHttpAdapter to self.session
        setup_session(self.session)

    def fetch(self, url):
        try:
            res = self.session.get(url)
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
