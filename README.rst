trequests
=========

A Tornado async HTTP/HTTPS client adaptor for python-requests.

The problem
-----------


The solution
------------


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
    
    # Tell requests to use our AsyncHTTPAdaptor for the default
    # session instance, you can also pass you own through
    setup_session()
    
    class WebHandler(RequestHandler):
        @tornalet
        def get(self):
            data = {'foo': 'bar'}
            # This will now unblock the current coroutine, like magic
            response = bobs_big_data.BigData(data).post()
            return self.write(response)
