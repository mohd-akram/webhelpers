"""HTML/XHTML Tag generator

You create tags with attribute access.  I.e., the "A" anchor tag is
html.a.  The attributes of the HTML tag are done with keyword
arguments.  The contents of the tag are the non-keyword arguments
(concatenated).  You can also use the special "c" keyword, passing a
list, tuple, or single tag, and it will make up the contents (this is
useful because keywords have to come after all non-keyword arguments,
and it's unintuitive to give your content before your attributes).

If the value of an attribute is None, then no attribute will be
inserted.  Think of it as "does not apply".  So::

    >>> HTML.a(href="http://www.yahoo.com", name=None, 
    ... c="Click Here")
    literal(u'<a href="http://www.yahoo.com">Click Here</a>')

If the value is None, then the empty string is used.  Otherwise str()
is called on the value.

``HTML`` can also be called, and it will concatenate the quoted string
representations of its arguments.

``HTML.comment`` will generate an HTML comment, like
``HTML.comment('comment text', 'and some more text')`` -- note that
it cannot take keyword arguments (because they wouldn't mean anything).

``HTML.literal`` will allow you to give HTML source without any quoting.

If you cannot define an attribute because it conflicts with a Python
keyword (particularly ``class``), you can append an underscore and
it will be removed (like ``class_='whatever'``).

"""
import re
from cgi import escape as cgi_escape
from urllib import quote as url_escape
from UserDict import DictMixin

class UnfinishedTag(object):
    
    """Represents an unfinished or empty tag."""
    
    def __init__(self, tag):
        """Initialize with the tag name."""
        self._tag = tag

    def __call__(self, *args, **kw):
        """Create the tag with the arguments passed in."""
        return make_tag(self._tag, *args, **kw)

    def __str__(self):
        """Return a literal representation."""
        return literal('<%s />' % self._tag)

    def __html__(self):
        """Return the HTML escaped tag."""
        return str(self)


class UnfinishedComment(object):
    
    """Represents an unfinished or empty comment."""
    
    def __call__(self, *args):
        """Create the HTML comment."""
        return literal('<!--%s-->' % ''.join(str(x) for x in args))
        
    def __html__(self):
        """Return the HTML escaped tag."""
        raise UnfinishedTag


class UnfinishedLiteral(object):
    
    """Represent an unfinished literal value."""
    
    def __call__(self, *args):
        """Return the literal HTML."""
        return literal(*args)

    def __html__(self):
        """Return the HTML escaped text."""
        raise UnfinishedTag


class Base(object):
    
    """Base HTML object."""
    
    comment = UnfinishedComment()
    literal = UnfinishedLiteral()
    
    def __getattr__(self, attr):
        """Generate the tag for the given attribute name."""
        if attr.startswith('_'):
            raise AttributeError
        result = self.__dict__[attr] = UnfinishedTag(attr.lower())
        return result

    def __call__(self, *args):
        """Join raw HTML and HTML escape it."""
        return ''.join(escape(x) for x in args)


def attrEncode(v):
    """Parse out attributes that begin with '_'."""
    if v.endswith('_'):
        return v[:-1]
    else:
        return v


def make_tag(tag, *args, **kw):
    if kw.has_key("c"):
        assert not args, "The special 'c' keyword argument cannot be used "\
"in conjunction with non-keyword arguments"
        args = kw.pop("c")
    htmlArgs = [' %s="%s"' % (attrEncode(attr), escape(value))
                for attr, value in sorted(kw.iteritems())
                if value is not None]
    if not args and emptyTags.has_key(tag):
        substr = '<%s%s />'
        if blockTags.has_key(tag):
            return literal(substr % (tag, "".join(htmlArgs)))
        else:
            return literal(substr % (tag, "".join(htmlArgs)))
    else:
        if blockTags.has_key(tag):
            return literal("<%s%s>%s</%s>" % (
                tag,
                "".join(htmlArgs),
                "".join(escape(x) for x in args),
                tag))
        else:
            return literal("<%s%s>%s</%s>" % (
                tag,
                "".join(htmlArgs),
                "".join(escape(x) for x in args),
                tag))


class literal(unicode):
    
    """Represents an HTML literal.
    
    This subclass of unicode has a ``.__html__()`` method that is 
    detected by the ``escape()`` function.
    
    Also, if you add another string to this string, the other string 
    will be quoted and you will get back another literal object.  Also
    ``literal(...) % obj`` will quote any value(s) from ``obj``.  If
    you do something like ``literal(...) + literal(...)``, neither
    string will be changed because ``escape(literal(...))`` doesn't
    change the original literal.
    
    """
    
    def __new__(cls, string='', encoding='utf-8', errors="strict"):
        """Create the new literal string object."""
        if isinstance(string, unicode):
            obj = unicode.__new__(cls, string)
        else:
            obj = unicode.__new__(cls, string, encoding, errors)
        obj.encoding = encoding
        obj.error_mode = errors
        return obj

    def __str__(self):
        return self.encode(self.encoding)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, unicode.__repr__(self))
        
    def __html__(self):
        return self
        
    def __add__(self, other):
        return self.__class__(unicode.__add__(self, escape(other)))
        
    def __radd__(self, other):
        if not isinstance(other, basestring):
            raise NotImplemented
        return self.__class__(unicode.__add__(escape(other), self))
    
    def __mul__(self, count):
        return self.__class__(unicode.__mul__(self, count))
    
    def __mod__(self, obj):
        if isinstance(obj, tuple):
            return unicode.__mod__(self, tuple(_EscapedItem(item, self.encoding, self.error_mode) for item in obj))
        else:
            return unicode.__mod__(self, _EscapedItem(obj, self.encoding, self.error_mode))
 
    def join(self, items):
        return self.__class__(unicode.join(self, (escape(i) for i in items)))


def lit_sub(*args, **kw):
    """Ensures that if the string re.sub operates on is a literal, it
    will still be a literal returned"""
    lit = hasattr(args[2], '__html__')
    cls = args[2].__class__
    result = re.sub(*args, **kw)
    if lit:
        return cls(result)
    else:
        return result


def escape(val, force=False):
    """Does HTML-escaping of a value.
    
    Objects with a ``.__html__()`` method will have that method called,
    and the return value will *not* be quoted.  Thus objects with that
    magic method can be used to represent HTML that should not be
    quoted.
    
    As a special case, ``escape(None)`` returns ''
    
    If ``force`` is true, then it will always be quoted regardless of
    ``__html__()``.
    
    """
    if val is None:
        return literal('')
    elif not force and hasattr(val, '__html__'):
        return literal(val.__html__())
    elif isinstance(val, basestring):
        return literal(cgi_escape(val, True))
    else:
        return literal(cgi_escape(unicode(val), True))

class _EscapedItem(DictMixin):
    
    """Wrapper/helper for literal(...) % obj
    
    This quotes the object during string substitution, and if the
    object is dictionary(-like) it will quote all the values in the
    dictionary.
    
    """
    
    def __init__(self, obj, encoding, error_mode):
        self.obj = obj
        self.encoding = encoding
        self.error_mode = error_mode
        
    def __getitem__(self, key):
        return _EscapedItem(self.obj[key], self.encoding, self.error_mode)
        
    def __str__(self):
        v = escape(self.obj)
        if isinstance(v, unicode):
            v = v.encode(self.encoding)
        return v
        
    def __unicode__(self):
        v = escape(self.obj)
        if isinstance(v, str):
            v = v.decode(self.encoding, self.error_mode)
        return v
    
    def __int__(self):
        return int(self.obj)
    
    def __float__(self):
        return float(self.obj)
    
    def __repr__(self):
        return escape(repr(self.obj))


emptyTagString = """
area base basefont br col frame hr img input isindex link meta param
"""

emptyTags = {}
for tag in emptyTagString.split():
    emptyTags[tag] = 1

blockTagString = """
applet blockquote body br dd div dl dt fieldset form frameset
head hr html iframe map menu noframes noscript object ol optgroup
p param script select table tbody tfoot thead tr ul var
"""

blockTags = {}
for tag in blockTagString.split():
    blockTags[tag] = 1

HTML = Base()

__all__ = ["HTML", "escape", "literal", "url_escape"]
