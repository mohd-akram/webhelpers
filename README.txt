WebHelpers
++++++++++++

WebHelpers provides functions useful in web applications: generating HTML tags,
showing results a pageful at a time, etc.  It may be used with any web
framework or template engine.  

The biggest difference between WebHelpers 0.6 and previous versions is the new
HTML tag generator (``webhelpers.html``) which does smart HTML escaping.
``webhelpers.rails`` has been deprecated and most of its functions have been
reimplemented in new modules. All HTML helpers return a ``literal`` object,
which is a Unicode subclass.  [XXX explain this further, and ``literal()``.]


WebHelpers currently consists of the following
modules and packages under the ``webhelpers.`` namespace:

``date``
    Date/time helpers.  These currently format strings based on dates.

``feedgenerator``
    A syndication feed library, used for generating RSS, Atom, etc.
    Ported from Django.

``html``
    A library for generating HTML tags, written by Ian Bicking.  Unlike
    ElementTree it can produce HTML fragments and has a pythonic API. Unlike
    lxml it's pure Python and has no dependencies.  It also does smart HTML
    escaping, described below.  

``markdown``
    A text to HTML converter.  Normally invoked via
    ``webhelpers.tools.markdown()``.  (If you use this library directly, you
    may have to wrap return values in ``literal()`` to prevent them from
    being double escaped.)

``paginate``
    A tool for letting you view a large sequence a screenful at a time,
    with previous/next links.
    

``string24``
    The ``string`` module from Python 2.4.  Useful if you're running on
    Python 2.3.

``tags``
    Helpers producing simple HTML tags.

``text``
    Helpers producing string output, suitable for both HTML and non-HTML
    applications.

``textile``
    Another text to HTML converter.  Normally invoked via
    ``webhelpers.tools.textilize()``.  (If you use this library directly, you
    may have to wrap return values in ``literal()`` to prevent double
    escaping.)

``tools``
    Helpers producing complex chunks of HTML.

``util``
    Miscellaneous functions.

The following modules/packages are deprecated and will be removed in a future
version of WebHelpers:

``commands``
    Contains a ``distutils`` plugin to compress Javascript/CSS for
    transmission. This version is buggy; the WebHelpers developers are
    investigating alternatives.

``hinclude``
    Client-side include via Javascript. Deprecated because it uses 
    ``webhelpers.rails`` and is trivial.

``htmlgen``
    Older version of ``webhelpers.html``, without smart escaping.

``pagination``
    Older version of ``webhelpers.paginate``.

``rails``
    A large number of functions ported from Rails.  Most of these have been
    reimplemented in other WebHelpers modules to take advantage of
    ``webhelpers.html`` and smart escaping.  (Some of the rails functions are
    prone to double HTML escaping.)  Includes the "Prototype" and
    "Scriptaculous" Javascript libraries, which are unsupported.  This package
    depends on Routes.

WebHelpers is package aimed at providing helper functions for use within web
applications.

These functions are intended to ease web development with template languages by
removing common view logic and encapsulating it in re-usable modules as well as
occasionally providing objects for use within controllers to assist with common
web development paradigms.

For support/question/patches, please use the `Pylons mailing list
<http://groups.google.com/group/pylons-discuss>`_.

*Requirements:* Some WebHelper functions require `Routes
<http://routes.groovie.org/>`_ to be active in the framework for a variety of
functions. Currently `Pylons <http://pylons.groovie.org/>`_, `TurboGears
<http://trac.turbogears.org/turbogears/wiki/RoutesIntegration>`_, and `Aquarium
<http://aquarium.sourceforge.net/>`_ support Routes.

Update 2008-04-29
-----------------
helpers.patch addresses some of the issues in helpers.py.

test_mail.py is a test suite for webhelpers.mail.  It depends on an SMTP server
being available, so we're unsure how to integrate it with the standard test
suite.  

wsgiapp_image.jpg is a file used by test_mail.py.
