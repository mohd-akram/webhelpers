"""Functions that output text (not HTML).

Provides methods for filtering, formatting and transforming strings.
"""

import re

from html import HTML, literal, escape
import webhelpers.textile as textile
import webhelpers.markdown as _markdown

AUTO_LINK_RE = re.compile(r"""
                        (                          # leading text
                          <\w+.*?>|                # leading HTML tag, or
                          [^=!:'"/]|               # leading punctuation, or 
                          ^                        # beginning of line
                        )
                        (
                          (?:https?://)|           # protocol spec, or
                          (?:www\.)                # www.*
                        ) 
                        (
                          [-\w]+                   # subdomain or domain
                          (?:\.[-\w]+)*            # remaining subdomains or domain
                          (?::\d+)?                # port
                          (?:/(?:(?:[~\w\+%-]|(?:[,.;:][^\s$]))+)?)* # path
                          (?:\?[\w\+%&=.;-]+)?     # query string
                          (?:\#[\w\-]*)?           # trailing anchor
                        )
                        ([\.,"'?!;:]|\s|<|$)       # trailing text
                           """, re.X)
    

def truncate(text, length=30, truncate_string='...'):
    """
    Truncate ``text`` with replacement characters.
    
    ``length``
        The maximum length of ``text`` before replacement
    ``truncate_string``
        If ``text`` exceeds the ``length``, this string will replace
        the end of the string

    Example::

        >>> truncate('Once upon a time in a world far far away', 14)
        'Once upon a...'
        
    """
    if not text: return ''
    
    new_len = length-len(truncate_string)
    if len(text) > length:
        return text[:new_len] + truncate_string
    else:
        return text

def highlight(text, phrase, highlighter='<strong class="highlight">\\1</strong>'):
    """
    Highlight the ``phrase`` where it is found in the ``text``.
    
    The highlighted phrase will be surrounded by the highlighter, 
    by default::
    
        <strong class="highlight">I'm a highlight phrase</strong>
    
    ``highlighter``
        Defines the highlighting phrase. This argument should be a 
        single-quoted string with ``\\1`` where the phrase is supposed 
        to be inserted.
        
    Note: The ``phrase`` is sanitized to include only letters, digits, 
    and spaces before use.

    Example::

        >>> highlight('You searched for: Pylons', 'Pylons')
        'You searched for: <strong class="highlight">Pylons</strong>'
        
    """
    if not phrase or not text:
        return text
    highlight_re = re.compile('(%s)' % re.escape(phrase), re.I)
    return highlight_re.sub(highlighter, text)

def excerpt(text, phrase, radius=100, excerpt_string="..."):
    """
    Extract an excerpt from the ``text``, or '' if the phrase isn't found.

    ``phrase``
        Phrase to excerpt from ``text``
    ``radius``
        How many surrounding characters to include
    ``excerpt_string``
        Characters surrounding entire excerpt
    
    Example::
    
        >>> excerpt("hello my world", "my", 3)
        '...lo my wo...'
        
    """
    if not text or not phrase:
        return text

    pat = re.compile('(.{0,%s}%s.{0,%s})' % (radius, re.escape(phrase), radius), re.I)
    match = pat.search(text)
    if not match:
        return ""
    excerpt = match.expand(r'\1')
    if match.start(1) > 0:
        excerpt = excerpt_string + excerpt
    if match.end(1) < len(text):
        excerpt = excerpt + excerpt_string
    return excerpt

def auto_link(text, link="all", **href_options):
    """
    Turn all urls and email addresses into clickable links.
    
    ``link``
        Used to determine what to link. Options are "all", 
        "email_addresses", or "urls"
    
    Example::
    
        >>> auto_link("Go to http://www.planetpython.com and say hello to guido@python.org")
        literal(u'Go to <a href="http://www.planetpython.com">http://www.planetpython.com</a> and say hello to <a href="mailto:guido@python.org">guido@python.org</a>')
        
    """
    if not text:
        return u""
    if link == "all":
        return _auto_link_urls(_auto_link_email_addresses(text), **href_options)
    elif link == "email_addresses":
        return _auto_link_email_addresses(text)
    else:
        return _auto_link_urls(text, **href_options)

def _auto_link_urls(text, **href_options):
    def handle_match(matchobj):
        all = matchobj.group()
        before, prefix, link, after = matchobj.group(1, 2, 3, 4)
        if re.match(r'<a\s', before, re.I):
            return all
        text = literal(prefix + link)
        if prefix == "www.":
            prefix = "http://www."
        a_options = dict(href_options)
        a_options['href'] = literal(prefix + link)
        return literal(before) + HTML.a(text, **a_options) + literal(after)
    return literal(re.sub(AUTO_LINK_RE, handle_match, text))

def _auto_link_email_addresses(text):
    return re.sub(r'([\w\.!#\$%\-+.]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+)',
                  r'<a href="mailto:\1">\1</a>', text)

def markdown(text, **kwargs):
    """Format the text with MarkDown formatting.
    
    This function uses the `Python MarkDown library 
    <http://www.freewisdom.org/projects/python-markdown/>`_
    which is included with WebHelpers.
    
    """
    return _markdown.markdown(text, **kwargs)

def textilize(text, sanitize=False):
    """Format the text with Textile formatting.
    
    This function uses the `PyTextile library <http://dealmeida.net/>`_ 
    which is included with WebHelpers.
    
    Additionally, the output can be sanitized which will fix tags like 
    <img />,  <br /> and <hr /> for proper XHTML output.
    
    """
    texer = textile.Textiler(text)
    return texer.process(sanitize=sanitize)

def strip_links(text):
    """
    Strip link tags from ``text`` leaving just the link label.
    
    Example::
    
        >>> strip_links('<a href="something">else</a>')
        'else'
        
    """
    if isinstance(text, literal):
        lit = literal
    else:
        lit = lambda x: x
    strip_re = re.compile(r'<a\b.*?>(.*?)<\/a>', re.I | re.M)
    return lit(strip_re.sub(r'\1', text))

__all__ = ['truncate', 'highlight', 'markdown', 'strip_links',
       'auto_link', 'excerpt', 'textilize']
