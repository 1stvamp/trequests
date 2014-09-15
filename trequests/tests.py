import requests
from tornalet import tornalet
from trequests import setup_session
from tornado.ioloop import IOLoop
from tornado.escape import json_decode
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, RequestHandler

setup_session()


class TestUtil(object):

    def send(self, data):
        return requests.post('http://httpbin.org/post', data=data).json()


class TestHandler(RequestHandler):

    @tornalet
    def get(self):
        util = TestUtil()
        data = {'foo': 'bar'}
        response = util.send(data)
        self.write(response)


class TestCase(AsyncHTTPTestCase):

    def setUp(self):
        self.application = None
        super(TestCase, self).setUp()
        self.get_app().callback_called = False

    def get_new_ioloop(self):
        return IOLoop().instance()

    def get_app(self):
        if not self.application:
            self.application = Application(
                [(r'/', TestHandler)]
            )

        return self.application

    def _test_callback(self):
        self.get_app().callback_called = True

    def test_post(self):
        """Test using a library that POSTs to requestbin using requests.
        """

        self.get_new_ioloop().add_callback(self._test_callback)
        response = self.fetch('/')
        data = json_decode(response.body)

        self.assertEqual(response.code, 200)
        self.assertEqual(data['form']['foo'], 'bar')
        self.assertTrue(self.get_app().callback_called)
