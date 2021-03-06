What's New in WebHelpers
========================

This is a high-level overview of recent changes. **Incompatible changes are
in boldface;** these may require modifying your application.  See `Changelog
<changelog.html>`_ for the full changelog.

Version 1.3
-----------

*webhelpers.paginate*: Add URL generator classes for new frameworks like
Pyramid.

*webhelpers.html.grid*: Add ability to use URL generator classes for paged
display.

*webhelpers.pylonslib.grid*: Deprecated. Use webhelpers.html.grid, which now
supports paged display.

Version 1.2
-----------

*webhelpers.html:* The HTML builder now uses Armin Ronacher's
"MarkupSafe" package, which Mako and Pylons have also switched to.  MarkupSafe
has a C speedup for escaping, escapes single-quotes for greater security (to
close a potential XSS attack route), and adds new methods to ``literal``.
**literal** is now a subclass of ``markupsafe.Markup``;
**escape** is a wrapper for ``markupsafe.escape_silent``.

*webhelpers.html.tags:* The ``text()`` helper has a "type" argument for new
HTML 5 input types.

*webhelpers.html.tags:* **No longer adds an "id" attribute to hidden fields
generated by the ``form()`` helper**, to prevent IDs from clashing if the page
contains multiple forms. To create a hidden field with an ID, call ``hidden()``
directly.

*webhelpers.util:* ``update_params`` now supports query parameters with
multiple values.

Version 1.1
-----------

*webhelpers.pylonslib.minify*: The Javascript minification code was removed
due to a non-free license. **The helper now minifies Javascript only if the
"jsmin" package is installed.**  Otherwise it issues a warning and leaves the
Javascript unchanged. CSS minification is not affected. Details are in
webhelpers/pylonslib/_minify.py .

Version 1.0
-----------

WebHelpers 1.0 has a lot of new features compared to 0.6.4. Several modules
deprecated in 0.6.4 were removed, but otherwise there are only a few API
incompatibilities with the 0.6 series.

Deleted packages
++++++++++++++++

**The following deprecated packages were removed: rails, commands, hinclude,
htmlgen, pagination, and string24.** Most of the functionality of the rails
helpers was replaced by new helpers in the ``date``, ``html``, ``misc``,
``number``, and ``text`` packages. Prototype and Scriptaculous are not
replaced; WebHelpers no longer ships with Javascript libraries.  ``pagination``
was replaced by ``paginate``.  ``number_to_human_size()`` is in the unfinished
directory in the source distribution; you can copy it to your application if
you need it.  If you can't switch to the replacement helpers,
stick with WebHelpers 0.6.4.

secure_form
+++++++++++

**webhelpers.html.secure_form was moved to
webhelpers.pylonslib.secure_form because it depends on Pylons.**

webhelpers.constants
++++++++++++++++++++

**uk_counties() now returns tuples rather than strings.**

webhelpers.feedgenerator
++++++++++++++++++++++++

``webhelpers.feedgenerator`` was upgraded to the Django original (December 2009
version), and the "Geo" classes were added for geographical (GIS) feeds.
Points are latitude/longitude by default, but there's a flag if your data is
longitude first (as Django is). A ``Geometry`` class was reverse engineered for
other geometries, but it's untested.  Add a "published" property for Atom
feeds.

webhelpers.html.builder
+++++++++++++++++++++++

New method for producing CDATA sections.  The basic tag builders have a ``_nl``
flag to add a newline between content elements and after the tag for
readability.

webhelpers.html.converters
++++++++++++++++++++++++++

``markdown()`` adds an argument to choose a Markdown implementation.
The Markdown included in WebHelpers will remain at version 1.7, but Markdown
2.x is available on PyPI, and a separate implementation confusingly called
"Markdown2" is also available on PyPI.

webhelpers.html.render
++++++++++++++++++++++

New helpers to render HTML to text, and to sanitize user input by stripping
HTML tags.

webhelpers.html.tags
++++++++++++++++++++

New helpers to add CSS classes to a tag
programmatically, to support option groups in <select> tags, and to generate
<!doctype> and <?xml ?> declarations.

``image()`` can calculate the width and height of an image automatically, using
either the Python Imaging Library (PIL) or a pure Python algorithm in
``webhelpers.media``. 

``form()`` puts its hidden "_method" field in a <div> for
XHTML compliance, and the ``hidden()`` helper has a magic ID attribute to match
the other helpers.

webhelpers.html.tools
+++++++++++++++++++++

Ported ``js_obfuscate()`` from the old rails helpers.

``highlight()`` adds new arguments for flexibility, and
is reimplemented using the HTML builder. **The 'highlighter' argument is
deprecated.**

webhelpers.misc
+++++++++++++++

New helpers to flatten nested lists and tuples, and to
gather all the subclasses of a specified class. There's an exception
``OverwriteError``, a ``DeclarativeException`` class for making your own
exceptions with constant messages, and a ``deprecate`` function.

webhelpers.number
+++++++++++++++++
``format_data_size()`` and its derivatives ``format_byte_size()`` and
``format_bit_size()`` provide a convenient way to display numbers using SI
units ("1.2 kilobytes", "1.2 kB", "1.0 KiB").

webhelpers.paginate
+++++++++++++++++++

``webhelpers.paginate`` has a new algorithm for generating URLs for page links,
has some enhancements for Javascript, works with all versions of SQLAlchemy 0.4
and higher, and has a presliced list option.

On Pylons it will use ``pylons.url.current`` as the URL generator, or fall back
to ``routes.url_for`` if that is not available. You can also pass a callback
function to the constructor to implement a custom generator. If none of these
are available, you'll get a ``NotImplementedError``. Previous versions of
WebHelpers (through 1.0b5) used ``routes.url_for`` unconditionally, but that
function is deprecated and is not supported in Pylons 1.x.

webhelpers.pylonslib
++++++++++++++++++++

``webhelpers.pylonslib`` is now a package. The ``Flash`` class accepts severity
categories, which you can use to style more severe messages differently. **The
session structure is different, so delete existing HTTP sessions when
upgrading.**

webhelpers.text
++++++++++++++++

``webhelpers.text`` adds a suite of helpers from Ruby's stringex package to
convert strings to URL-friendly format, and to remove inconvenient accents from
characters, etc.

webhelpers.util
+++++++++++++++

New helper to update the query parameters in a URL.

Experimental code
+++++++++++++++++

``webhelpers.html.grid`` and ``webhelpers.pylonslib.grid`` contain helpers to
make an HTML table from a list of objects such as database records. It has
a demo program and an optional stylesheet.  It's "experimental" because the
docs aren't very clear and the API could maybe do with some changes.  But it works.

``webhelpers.pylonslib.minify`` contains versions of ``javascript_link()`` and
``stylesheet_link()`` that compress their files. It's experimental because
their tests fail, so they probably don't work.

Other experiments are in the "unfinished" directory in the source distribution.
