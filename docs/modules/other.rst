Non-essential modules
=====================

``webhelpers.markdown`` is a copy of Markdown 1.7, used as a fallback for
``webhelpers.html.converters.markdown()`` if the full Markdown package is not
installed. See the `Markdown <>` website for documentation on the Markdown
format and this module.  Markdown is now at version 2.x and contains new
features and plugins which are too big to include in WebHelpers. There is also
an alternate implementation called Markdown2.  Both are available on PyPI.  See
the ``markdown()`` documentation for how to use them with WebHelpers.

``webhelpers.textile`` is a copy of Textile, used by
``webhelpers.html.converters.textilize()``.  See the `Textile <>`_ site for
documentation on the Textile format and this module.

``webhelpers.string24`` is a copy of Python 2.4's ``string`` module, for
programs still running on Python 2.3.  It will be removed in a future version
of WebHelpers.
