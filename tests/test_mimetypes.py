from nose.plugins.skip import SkipTest

from webhelpers.mimehelper import MIMETypes
from util import test_environ

def _check_webob_dependency():
    try:
        import webob
    except ImportError:
        raise SkipTest("WebOb not installed; skipping test")

def setup():
    MIMETypes.init()

def test_register_alias():
    MIMETypes.add_alias('html', 'text/html')
    assert MIMETypes.aliases['html'] == 'text/html'
    
def test_usage():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/test.html'
    m = MIMETypes(environ)
    assert m.mimetype('html') == 'text/html'

def test_root_path():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/'
    environ['HTTP_ACCEPT'] = 'text/html, application/xml'
    m = MIMETypes(environ)
    assert m.mimetype('text/html') == 'text/html'

def test_with_extention():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/test.xml'
    environ['HTTP_ACCEPT'] = 'text/html, application/xml'
    m = MIMETypes(environ)
    assert m.mimetype('text/html') == False
    assert m.mimetype('application/xml') == 'application/xml'

def test_with_unregistered_extention():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/test.iscool'
    environ['HTTP_ACCEPT'] = 'application/xml'
    m = MIMETypes(environ)
    assert m.mimetype('text/html') == False
    assert m.mimetype('application/xml') == 'application/xml'

def test_with_no_extention():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/test'
    environ['HTTP_ACCEPT'] = 'application/xml'
    m = MIMETypes(environ)
    assert m.mimetype('text/html') == False
    assert m.mimetype('application/xml') == 'application/xml'
    
def test_with_no_extention_and_no_accept():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/test'
    m = MIMETypes(environ)
    assert m.mimetype('html') == 'text/html'

def test_with_text_star_accept():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/test.iscool'
    environ['HTTP_ACCEPT'] = 'text/*'
    m = MIMETypes(environ)
    assert m.mimetype('text/html') == 'text/html'

def test_with_star_star_accept():
    _check_webob_dependency()
    environ = test_environ()
    environ['PATH_INFO'] = '/test.iscool'
    environ['HTTP_ACCEPT'] = '*/*'
    m = MIMETypes(environ)
    assert m.mimetype('application/xml') == 'application/xml'
