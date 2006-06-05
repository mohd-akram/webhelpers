"""
Javascript Helpers

Provides functionality for working with JavaScript in your views.

Ajax, controls and visual effects
---------------------------------

* For information on using Ajax, see `Prototype Helpers <module-railshelpers.helpers.prototype.html>`_.
* For information on using controls and visual effects, see `Scriptaculous Helpers <module-railshelpers.helpers.scriptaculous.html>`_.
"""
import os
import re
from tags import *

# The absolute path of the WebHelpers javascripts directory
javascripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'javascripts')

def link_to_function(name, function, **html_options):
    """
    Returns a link that'll trigger a JavaScript ``function`` using the 
    onclick handler and return false after the fact.
    
    Example::
    
        link_to_function("Greeting", "alert('Hello world!')")
    """
    options = dict(href="#", onclick="%s; return false;" % function)
    options.update(html_options)
    return content_tag("a", name, **options)

def button_to_function(name, function, **html_options):
    """
    Returns a link that'll trigger a JavaScript ``function`` using the 
    onclick handler and return false after the fact.
    
    Example::
    
        button_to_function("Greeting", "alert('Hello world!')")
    """
    options = dict(type_="button", value=name, onclick="%s; " % function)
    options.update(html_options)
    return content_tag("input", "", **options)

def escape_javascript(javascript):
    """
    Escape carriage returns and single and double quotes for JavaScript segments.
    """
    javascript = re.sub(r'\r\n|\n|\r', r'\\n', (javascript or ''))
    javascript = re.sub(r'(["\'])', r'\\\1', javascript)
    return javascript

def javascript_tag(content):
    """
    Returns a JavaScript tag with the ``content`` inside.
    
    Example::
    
        >>> javascript_tag("alert('All is good')"
        '<script type="text/javascript">alert('All is good')</script>'
    """
    return content_tag("script", javascript_cdata_section(content), type="text/javascript")

def javascript_cdata_section(content):
    return "\n//%s\n" % cdata_section("\n%s\n//" % content)

def options_for_javascript(options):
    optionlist = []
    for key, value in options.iteritems():
        if isinstance(value, bool):
            value = str(value).lower()
        optionlist.append('%s:%s' % (key, value))
    optionlist.sort()
    return '{' + ', '.join(optionlist) + '}'

def array_or_string_for_javascript(option):
    jsoption = None
    if isinstance(option, list):
        jsoption = "['%s']" % '\',\''.join(option)
    elif isinstance(option, bool):
        jsoption = str(option).lower()
    else:
        jsoption = "'%s'" % option
    return jsoption

__all__ = ['button_to_function', 'javascript_tag', 'escape_javascript', 'link_to_function']
