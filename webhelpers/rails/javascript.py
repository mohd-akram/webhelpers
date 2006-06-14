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
from routes import request_config

# The absolute path of the WebHelpers javascripts directory
javascript_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'javascripts')

# WebHelpers' built-in javascripts. Note: scriptaculous automatically includes all of its
# supporting .js files
javascript_builtins = ('prototype.js', 'scriptaculous.js')

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

def javascript_include_tag(*sources, **options):
    """
    Returns script include tags for the specified javascript ``sources``.

    Each source's URL path is prepended with '/javascripts/' unless their full path is
    specified. Each source's URL path is ultimately prepended with the environment's
    ``SCRIPT_NAME`` (the root path of the web application).

    Optionally includes (prepended) WebHelpers' built-in javascripts when passed the
    ``builtins=True`` keyword argument.

    Examples::
    
        >>> print javascript_include_tag(builtins=True)
        <script src="/javascripts/prototype.js" type="text/javascript"></script>
        <script src="/javascripts/scriptaculous.js" type="text/javascript"></script>

        >>> print javascript_include_tag('prototype.js', '/other-javascripts/util.js')
        <script src="/javascripts/prototype.js" type="text/javascript"></script>
        <script src="/other-javascripts/util.js" type="text/javascript"></script>

        >>> print javascript_include_tag('app.js', '/test/test.js', builtins=True)
        <script src="/javascripts/prototype.js" type="text/javascript"></script>
        <script src="/javascripts/scriptaculous.js" type="text/javascript"></script>
        <script src="/javascripts/app.js" type="text/javascript"></script>
        <script src="/test/test.js" type="text/javascript"></script>
    """
    if options.get('builtins'):
        sources = javascript_builtins + sources
        
    # Prefix apps deployed under any SCRIPT_NAME path
    script_name = ''
    config = request_config()
    if hasattr(config, 'environ'):
        script_name = config.environ.get('SCRIPT_NAME', '')

    include_tags = []
    format_source = lambda s: s.startswith('/') and '%s%s' % (script_name, s) or \
        '%s/javascripts/%s' % (script_name, s)
    [include_tags.append(content_tag('script', None, **dict(type='text/javascript',
                                                            src=format_source(source)))) \
     for source in sources]
    return '\n'.join(include_tags)

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

__all__ = ['javascript_path', 'javascript_builtins', 'link_to_function', 'button_to_function',
           'escape_javascript', 'javascript_tag', 'javascript_include_tag']
