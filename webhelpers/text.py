"""Functions that output text (not HTML).

Helpers for filtering, formatting, and transforming strings.
"""

import re

__all__ = ["truncate", "excerpt"]

def truncate(text, length=30, truncate_string='...'):
    """Truncate ``text`` with replacement characters.
    
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

def excerpt(text, phrase, radius=100, excerpt_string="..."):
    """Extract an excerpt from the ``text``, or '' if the phrase isn't
    found.

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

    pat = re.compile('(.{0,%s}%s.{0,%s})' % (radius, re.escape(phrase), 
                                             radius), re.I)
    match = pat.search(text)
    if not match:
        return ""
    excerpt = match.expand(r'\1')
    if match.start(1) > 0:
        excerpt = excerpt_string + excerpt
    if match.end(1) < len(text):
        excerpt = excerpt + excerpt_string
    if hasattr(text, '__html__'):
        return literal(excertp)
    else:
        return excerpt

