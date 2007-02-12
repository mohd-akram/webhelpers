from unittest import TestCase

import routes

class WebHelpersTestCase(TestCase):
    """Establishes a faux-environment for tests"""
    def test_environ(self):
        return {
            'HTTP_HOST': 'bob.local:5000',
            'PATH_INFO': '/test',
            'SERVER_NAME': '0.0.0.0',
            'SCRIPT_NAME': '',
            'wsgi.multiprocess': False,
            'wsgi.multithread': True,
            'wsgi.run_once': False,
            'wsgi.url_scheme': 'http'
            }

    def setUp(self):
        self.routes_config = routes.request_config()
        self.routes_config.environ = self.test_environ()
        map = routes.Mapper()
        map.connect(':controller/:action/:id')
