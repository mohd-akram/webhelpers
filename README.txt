WebHelpers
++++++++++++

WebHelpers provides functions useful in web applications: generating HTML tags,
showing results a pageful at a time, etc.  It may be used with any web
framework or template engine.  

The biggest difference between WebHelpers 0.6 and previous versions is the new
HTML tag generator with smart escaping, and the new helpers written to replace
the deprecated ``webhelpers.rails``.  A brief summary of the module layout is
below; see the docstrings in the source for documentation.

``constants``
    Country codes, states and provinces.

``containers``
    High-level container objects and dict/list helpers.

``date``
    Date/time helpers.  These currently format strings based on dates.

``feedgenerator``
    A syndication feed library, used for generating RSS, Atom, etc.
    Ported from Django.

``html``
    A package of HTML-related helpers.

    ``html.builder``
        A library for generating HTML tags with smart escaping.  All
        public symbols are imported into ``webhelpers.html``.

    ``converters``
        Text-to-HTML converters.

    ``tags``
        High-level HTML tags, including form tags, hyperlinks, and 
        Javascript/CSS links.  The ``ModelTags`` class builds input
        tags from database records (for any kind of database).

    ``tools``
        Helpers producing chunks of HTML.

``markdown``
    A text to HTML converter.  Normally invoked via
    ``webhelpers.tools.markdown()``.  (If you use this library directly, you
    may have to wrap the results in ``literal()`` to prevent double escaping.)

``media``
    Helpers for images, PDFs, etc.

``misc``
    Miscellaneous helpers that are neither text, numeric, container, or date.

``number``
    Numeric helpers and number formatters.

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
    may have to wrap the results in ``literal()`` to prevent double escaping.)

``util``
    Miscellaneous functions.

WebHelpers is package aimed at providing helper functions for use within web
applications.

These functions are intended to ease web development with template languages by
removing common view logic and encapsulating it in re-usable modules as well as
occasionally providing objects for use within controllers to assist with common
web development paradigms.

For support/question/patches, please use the `Pylons mailing list
<http://groups.google.com/group/pylons-discuss>`_.

Requirements
------------

WebHelpers does not have any install dependencies, but some functions depend
on third-party libraries.

Routes_

    Version >= 1.7 but < 2.0 must be installed and running in the current
    web framework for:

    - webhelpers.html.tags (required only for ``javascript_link()``,
      ``stylesheet_link()``, or ``auto_discovery_link()`` functions).
    - webhelpers.paginate
    - the regression tests in the source distribution

    Currently Pylons_, TurboGears_, and Aquarium_ support Routes.

    A future version of WebHelpers will be compatible with Routes 2, which is
    still in development.

Pylons_

    The helpers in ``webhelpers.pylonslib`` depend on Pylons context variables
    (e.g., ``pylons.session``).  They can easily be reimplemented in another
    web framework if desired.

.. _Routes:  http://routes.groovie.org/
.. _Pylons:  http://pylonshq.com/
.. _TurboGears:  http://turbogears.org/
.. _Aquarium:  http://aquarium.sourceforge.net/
