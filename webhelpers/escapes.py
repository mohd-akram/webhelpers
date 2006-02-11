# $Id: escapes.py 2013 2005-12-31 03:19:39Z zzzeek $
# escapes.py - string escaping functions for Myghty
# Copyright (C) 2004, 2005 Michael Bayer mike_mp@zzzcomputing.com
# Original Perl code and documentation copyright (c) 1998-2003 by Jonathan Swartz. 
#
# This module is part of Myghty and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#


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
