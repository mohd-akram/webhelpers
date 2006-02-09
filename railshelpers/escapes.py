# $Id: escapes.py 2013 2005-12-31 03:19:39Z zzzeek $
# escapes.py - string escaping functions for Myghty
# Copyright (C) 2004, 2005 Michael Bayer mike_mp@zzzcomputing.com
# Original Perl code and documentation copyright (c) 1998-2003 by Jonathan Swartz. 
#
# This module is part of Myghty and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#


import cgi

def html_escape(string):
    return cgi.escape(string, True)
