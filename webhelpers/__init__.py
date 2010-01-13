"""WebHelpers contains a wide variety of functions for web applications.
It's pure Python and can be used with any web framework, and many of the
helpers are also useful in non-web applications.

WebHelpers includes the widely-used HTML tag builder with smart escaping and
convenience functions for common tags. These ensure the HTML tags are
syntactically correct and prevent cross-site scripting attacks. Convenience
functions for form input tags and other common tags are provided.

Other helpers perform text processing, display records a pageful at a time,
generate Atom/RSS feeds with geographical (GIS) data, handle MIME types,
calculate statistics, and more.  There are also high-level container types,
including a value counter and accumulator.  There are lists of country names,
country codes, US states, Canadian provinces, and UK counties.

WebHelpers requires Python 2.4 or higher. It has not yet been tested with 
Python 3.  WebHelpers has no formal dependencies; however, a few individual
helpers depend on 
`Routes <http://routes.groovie.org/>`_, 
`Unidecode <http://python.org/pypi/Unidecode/>`_, 
`WebOb <http://pythonpaste.org/webob>`_, or
`Pylons <a href="http://pylonshq.com/>`_,
as noted in their documentation.

The main criteria for adding new helpers are: 

* Is it useful in a wide variety of applications, especially web applications?

* Does it avoid dependencies outside the Python standard library, especially
  C extensions which are hard to install on Windows and Macintosh?

* Is it too small to be released as its own project, and is there no other
  Python project more appropriate for it?

WebHelpers was originally created as a utility package for Pylons. Many of the
helpers were ported from Ruby on Rails. Version 0.6 introduced the HTML tag
builder and deprecated the rails helpers; new subpackages were added to replace
the rails helpers. Version 1.0 builds on this with many additional helpers.
"""
