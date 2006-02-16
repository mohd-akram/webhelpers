"""Utility functions used by various web helpers"""
import cgi

def html_escape(s):
    """HTML-escape a string or object
    
    This converts any non-string objects passed into it to strings
    (actually, using ``unicode()``).  All values returned are
    non-unicode strings (using ``&#num;`` entities for all non-ASCII
    characters).
    
    None is treated specially, and returns the empty string.
    """
    if s is None:
        return ''
    if not isinstance(s, basestring):
        s = unicode(s)
    s = cgi.escape(s, True)
    if isinstance(s, unicode):
        s = s.encode('ascii', 'xmlcharrefreplace')
    return s

class Partial(object):
    """partial object, which will be in Python 2.5"""
    def __init__(*args, **kw):
        self = args[0]
        self.fn, self.args, self.kw = (args[1], args[2:], kw)
    
    def __call__(self, *args, **kw):
        if kw and self.kw:
            d = self.kw.copy()
            d.update(kw)
        else:
            d = kw or self.kw
        return self.fn(*(args + self.args), **d)
