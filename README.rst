trequests
=========

.. image:: https://travis-ci.org/1stvamp/trequests.png?branch=master

A Tornado async HTTP/HTTPS client adapter for python-requests.

The problem
-----------

You enjoy using `Tornado <http://www.tornadoweb.org/>`_ to build fast non-blocking web applications, and you want to use a library from PyPI that makes a few HTTP requests, but pretty much every dev and their dog uses `Requests <http://python-requests.org/>`_ to make HTTP requests (rightly so, because it's *awesome*), but requests has no knowledge of the event loop nor can it yield when a socket blocks, which means any time you try to use a library like that it begins to block your request handling and grud-knows what other worlds of pain.

The solution
------------

Luckily there are solutions, one such is to use the `greenlet <http://greenlet.readthedocs.org/>`_ module to wrap blocking operations and swap Tornado coroutines at the right time, there is even the handy `tornalet <https://github.com/Gawen/tornalet>`_ module which handles this for you.

To make life even easier, you lucky lucky people, I've created ``trequests``, an async Requests adapter which uses greenlets (via tornalet) and the inbuilt non-blocking HTTP client methos in Tornado, to make any call to a library (utilizing Requests) non-blocking.

Installation
------------

.. code-block:: bash
    
    $ pip install trequests
  
Usage
-----
  
.. code-block:: python
    
    # Assume bobs_big_data uses python-requests for HTTP requests
    import bobs_big_data
    
    from tornado.web import RequestHandler
    from trequests import setup_session
    from tornalet import tornalet
    
    # Tell requests to use our AsyncHTTPadapter for the default
    # session instance, you can also pass you own through
    setup_session()
    
    class WebHandler(RequestHandler):
        @tornalet
        def get(self):
            data = {'foo': 'bar'}
            # This will now unblock the current coroutine, like magic
            response = bobs_big_data.BigData(data).post()
            return self.write(response)


Caveats
-------

``trequests`` has been used in production in a large scale metrics application, and is a very small and quite simple module.

**However** I've released it as ``0.9.x`` mainly because it's missing 100% compatibility with the Requests adapter API, most noticeably *cookie jar* and *session* support, which I will improve (or please send me a pull request if you fancy adding support), and release as a ``1.x`` branch when I have the time.

Also at the moment the ``setup_session`` utility actually monkey patches the ``session`` utility functions in Requests, as this was the only way I could see to override the mounts on "default" session instances (e.g. those created for every call when a session isn't provided). I'm hoping to change this in the future.
