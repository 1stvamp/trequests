from os import path
from urlparse import urlparse

import requests
from tornado.httpclient import AsyncHTTPClient
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornalet import asyncify


def get_version_string():
    return open(path.join(path.dirname(__file__),
                          'trequests_version.txt'), 'r').read().strip()


def get_version():
    return get_version_string().split('.')


__version__ = get_version_string()

# Don't know how to handle this yet, so just mock it out for now
requests.adapters.extract_cookies_to_jar = lambda a, b, c: None


class AsyncHTTPAdapter(requests.adapters.HTTPAdapter):
    """A python-requests HTTP/HTTPS adapter that uses the Tornado
    AsyncHTTPClient and greenlets (via the tornalet library) to perform a
    non-blocking call inside the Tornado IOLoop whenever a
    requests.[get/post/put/delete/request]() call is made. It then wraps the
    tornado.httpclient.HTTPResponse as a requests.models.Response instance and
    returns so that any library calling requests gets what it expects (mostly).
    """

    def send(self, request, stream=False, timeout=None, verify=True,
             cert=None, proxies=None):
        http_client = AsyncHTTPClient()
        # This where the magic happens, tornalet.asyncify wraps the parent
        # call in a greenlet that can be swapped out the same as any
        # aync tornado IO handler call.
        if isinstance(http_client, SimpleAsyncHTTPClient):
            resp = asyncify(http_client.fetch)(request=request.url,
                                               method=request.method,
                                               body=request.body,
                                               headers=request.headers,
                                               validate_cert=verify,
                                               request_timeout=timeout,
                                               )
        else:  # only curl_httpclient support proxy
            proxy_host, proxy_port, proxy_username, proxy_password = self._parse_proxy_url(proxies)
            resp = asyncify(http_client.fetch)(request=request.url,
                                               method=request.method,
                                               body=request.body,
                                               headers=request.headers,
                                               validate_cert=verify,
                                               request_timeout=timeout,
                                               proxy_host=proxy_host,
                                               proxy_port=proxy_port,
                                               proxy_username=proxy_username,
                                               proxy_password=proxy_password,
                                               )

        # We probably don't get this from any of the tornado adaptors, so
        # we stub it out as Unknown
        resp.reason = 'Unknown'
        resp.content = resp.body
        r = self.build_response(request, resp)
        # Reset the code and content as they're not parsed by build_response
        r.status_code = resp.code
        r._content = resp.content
        r.url = resp.effective_url
        return r

    def _parse_proxy_url(self, proxies):
        proxy_host = proxy_port = proxy_username = proxy_password = None
        if proxies:
            if proxies.get('http', None):
                url = proxies['http']
            elif proxies.get('https', None):
                url = proxies['https']
        try:
            o = urlparse(url)
            proxy_host, proxy_port, proxy_username, proxy_password = o.hostname, o.port, o.username, o.password
            return proxy_host, proxy_port, proxy_username, proxy_password
        except Exception, e:
            return proxy_host, proxy_port, proxy_username, proxy_password


def setup_session(session=None, mounts=None, http_client=None):
    """Mount the AsyncHTTPAdapter for a given session instance,
    or for the default instance in python-requests, for a given set of mounts
    or just for the default HTTP/HTTPS protocols.
    """
    if http_client == "curl":  # choose CurlAsyncHTTPClient
        AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    if session is None:
        session = requests.session()
    if mounts is None:
        mounts = ('http://', 'https://')

    def _session():
        for mount in mounts:
            session.mount(mount, AsyncHTTPAdapter())

    if session is None:
        requests.session = requests.sessions.session = _session
    else:
        _session()
