"""Helpers producing simple HTML tags"""

import os
import re
import urllib
import urlparse

try:
    from routes import request_config
except ImportError:
    request_config = None

from webhelpers.html import escape, HTML, literal, url_escape

__all__ = [
           # Form tags
           "form", 
           "end_form", 
           "text", 
           "textarea", 
           "hidden", 
           "file",
           "password", 
           "text", 
           "checkbox", 
           "radiobutton", 
           "submit",
           "select", 
           "options_for_select", 
           # hyperlinks
           "link_to",
           "link_to_if",
           "link_to_unless",
           # Other tags
           "image",
           # Head tags
           "auto_discovery_link",
           "javascript_link",
           "javascript_path",
           "stylesheet_link",
           ]


def form(url, method="POST", multipart=False, **options):
    """Start a form tag that points the action to an url.
    
    The url options should be given either as a string, or as a 
    ``url()`` function. The method for the form defaults to POST.
    
    Options:

    ``multipart``
        If set to True, the enctype is set to "multipart/form-data".
    ``method``
        The method to use when submitting the form, usually either 
        "GET" or "POST". If "PUT", "DELETE", or another verb is used, a
        hidden input with name _method is added to simulate the verb
        over POST.
    
    """
    if multipart:
        options["enctype"] = "multipart/form-data"
    
    method_tag = literal("")

    if method.upper() in ['POST', 'GET']:
        options['method'] = method
    else:
        options['method'] = "POST"
        method_tag = HTML.input(
            type="hidden", id="_method", name_="_method", value=method)
    
    options["action"] = url
    options["_closed"] = False
    return HTML.form(method_tag, **options)


def end_form():
    """Output "</form>".
    
    Example::

        >>> end_form()
        literal(u'</form>')
    
    """
    return literal("</form>")


def text(name, value=None, **options):
    """Create a standard text field.
    
    ``value`` is a string, the content of the text field.
    
    Options:
    
    * ``disabled`` - If set to True, the user will not be able to use
        this input.
    * ``size`` - The number of visible characters that will fit in the
        input.
    * ``maxlength`` - The maximum number of characters that the browser
        will allow the user to enter.
    
    Remaining keyword options will be standard HTML options for the
    tag.
    
    """
    o = {'type': 'text', 'name_': name, 'id': name, 'value': value}
    o.update(options)
    return HTML.input(**o)


def hidden(name, value=None, **options):
    """Create a hidden field.
    
    Takes the same options as text_field.
    
    """
    options.update(dict(type="hidden", id=options.get('id', name), name=name,
                        value=value))
    return HTML.input(**options)


def file(name, value=None, **options):
    """Create a file upload field.
    
    If you are using file uploads then you will also need to set the 
    multipart option for the form.

    Example::

        >>> file('myfile')
        literal(u'<input id="myfile" name="myfile" type="file" />')
    
    """
    options.update(dict(type="file", id=options.get('id', name), name=name, 
                        value=value))
    return HTML.input(**options)


def password(name="password", value=None, **options):
    """Create a password field.
    
    Takes the same options as text_field.
    
    """
    options.update(dict(type="password", id=options.get('id', name), 
                        name=name, value=value))
    return HTML.input(**options)


def textarea(name, content='', **options):
    """Create a text input area.
    
    Options:
    
    * ``size`` - A string specifying the dimensions of the textarea.
    
    Example::
    
        >>> textarea("body", '', size="25x10")
        literal(u'<textarea cols="25" id="body" name="body" rows="10"></textarea>')
    
    """
    if 'size' in options:
        options["cols"], options["rows"] = options["size"].split("x")
        del options['size']
    o = {'name_': name, 'id': name}
    o.update(options)
    return HTML.textarea(content, **o)


def checkbox(name, value="1", checked=False, disabled=False, readonly=False,
             **options):
    """Create a check box.

    Example::
    
        >>> checkbox("hi")
        literal(u'<input id="hi" name="hi" type="checkbox" value="1" />')
    
    """
    o = {'type': 'checkbox', 'name': name, 'id': name, 'value': value}
    o.update(options)
    for option in ("checked", "disabled", "readonly"):
        if locals().get(option):
            o[option] = option
    return HTML.input(**o)


def radiobutton(name, value, checked=False, **options):
    """Create a radio button.
    
    The id of the radio button will be set to the name + ' ' + value to 
    ensure its uniqueness.
    
    """
    pretty_tag_value = re.sub(r'\s', "_", '%s' % value)
    pretty_tag_value = re.sub(r'(?!-)\W', "", pretty_tag_value).lower()
    html_options = {'type': 'radio', 'name': name, 
                    'id': '%s_%s' % (name, pretty_tag_value), 'value': value}
    html_options.update(options)
    if checked:
        html_options["checked"] = "checked"
    return HTML.input(**html_options)


def submit(value="Save changes", name='commit', **options):
    """Create a submit button with the text ``value`` as the caption."""
    o = {'type': 'submit', 'name': name, 'value': value }
    o.update(options)
    return HTML.input(**o)


def options_for_select(container, selected=None, function=None):
    """Create select options from a container (list, tuple, dict), or
    objects/dicts in a container.  The result should be placed inside a
    <select> tag pair.
    
    Accepts a container (list, tuple, dict) and returns a string of 
    option tags. Given a container where the elements respond to first 
    and last (such as a two-element array), the "lasts" serve as option 
    values and the "firsts" as option text. Dicts are turned into this 
    form automatically, so the keys become "firsts" and values become 
    lasts. If ``selected`` is specified, the matching "last" or element 
    will get the selected option-tag. ``Selected`` may also be an array 
    of values to be selected when using a multiple select.
    
    If the container has dicts or objects, it will use the ``function``
    which must be specified and applies this function to each object or
    dictionary in the container.  This function should return a tuple
    of the option text and value of the dict or object.
    
    Examples (call, result)::
    
        >>> options_for_select([["Dollar", "$"], ["Kroner", "DKK"]])
        '<option value="$">Dollar</option>\\n<option value="DKK">Kroner</option>'
        >>> options_for_select([ "VISA", "MasterCard" ], "MasterCard")
        '<option value="VISA">VISA</option>\\n<option selected="selected" value="MasterCard">MasterCard</option>'
        >>> options_for_select(dict(Basic="$20", Plus="$40"), "$40")
        '<option selected="selected" value="$40">Plus</option>\\n<option value="$20">Basic</option>'
        >>> options_for_select([ "VISA", "MasterCard", "Discover" ], ["VISA", "Discover"])
        '<option selected="selected" value="VISA">VISA</option>\\n<option value="MasterCard">MasterCard</option>\\n<option selected="selected" value="Discover">Discover</option>'
        >>> def make_elem(x):
        ...     return x.name, x.price
        ...
        >>> class myObj(object):
        ...     name = ""
        ...     price = ""
        ...
        >>> myObj1 = myObj()
        >>> myObj1.name = "Basic"
        >>> myObj1.price = "$20"
        >>> myObj2 = myObj()
        >>> myObj2.name = "Plus"
        >>> myObj2.price = "$40"
        >>> options_for_select([myObj1, myObj2], selected="$40", function=make_elem)
        '<option value="$20">Basic</option>\\n<option selected="selected" value="$40">Plus</option>'
        >>> def make_elem(x):
        ...     return x["name"], x["price"]
        >>> options_for_select([{"name":"Basic", "price":"$20"},{"name":"Plus","price":"$40"}], selected="$40", function=make_elem)
        '<option value="$20">Basic</option>\\n<option selected="selected" value="$40">Plus</option>'
        
    Note: Only the option tags are returned.  You have to wrap this call 
    in a regular HTML select tag.
    
    """
    options = []
    if (not container):
        return ''
    
    if (not isinstance(selected, (list, tuple))):
        selected = (selected, )

    if (hasattr(container, 'values')):
        container = container.items()

    elif (isinstance(container[0], (dict, object))):
        if (function):
            container = [function(x) for x in container]

    if (not isinstance(container[0], (list, tuple))):
        container = [(x, x) for x in container]
        
    for x in container:
        if (x[1] in selected):
            options.append(str(HTML.option(x[0], value=x[1], selected="selected")))
        else:
            options.append(str(HTML.option(x[0], value=x[1])))
            
    return "\n".join(options)


def select(*args, **kw):
    # @@MO: Combine webhelpers.rails.form_tag.select with 
    # options_for_select above.  If the container value is a string, use it
    # as is; otherwise call options_for_select(container, selected, function).
    # Use the HTML object to create all tags.
    raise NotImplementedError()


#### Hyperlink tags

def link_to(label, url='', **html_options):
    """Create a hyperlink with the given text pointing to the URL.
    
    If the label is ``None`` or empty, the URL will be used as the label.

    This function does not modify the URL in any way.
    """
    """
    *THE FOLLOWING IS NOT IMPLEMENTED.  THIS IS NOT THE DOCSTRING.*
    
    See the valid options in the documentation for Routes url_for.
        
    Optionally you can make the link do a POST request (instead of the
    regular GET) through a dynamically added form element that is
    instantly submitted. Note that if the user has turned off
    Javascript, the request will fall back on the GET. So its your
    responsibility to determine what the action should be once it
    arrives at the controller.
    
    The POST form is turned on by passing ``post`` as True. Note, it's
    not possible to use POST requests and popup targets at the same
    time (an exception will be thrown).
    
    Examples::
    
        >> link_to("Delete this page", url(action="destroy", id=4))
        >> link_to("Destroy account", url(action="destroy"), 
        .. method='delete')
        
    """
    if callable(url):
        url = url()
    html_options['href'] = url
    return HTML.a(label or url, **html_options)


def link_to_if(condition, label, url='', **html_options):
    """Same as ``link_to`` but return just the label if the condition is false.
    
    This is useful in a menu when you don't want the current option to be a
    link.
    """
    if condition:
        return link_to(label, url, **html_options)
    else:
        return label

def link_to_unless(condition, label, url='', **html_options):
    """Same as ``link_to`` but return just the label if the condition is true.
    """
    if not condition:
        return link_to(label, url, **html_options)
    else:
        return label



#### Non-form tags

def image(source, alt=None, height=None, width=None, **options):
    """Return an image tag for the specified ``source``.

    ``source``
        The source URL of the image. The URL is prepended with 
        '/images/', unless its full path is specified. The URL is
        ultimately prepended with the environment's ``SCRIPT_NAME``
        (the root path of the web application), unless the URL is 
        fully-fledged (e.g. http://example.com).
    
    ``alt``
        The img's alt tag. Defaults to the source's filename, title
        cased.

    ``height``
        The height of the image, default is not included
        
    ``width``
        The width of the image, default is not included
        
    Examples::

        >>> image('xml.png')
        literal(u'<img alt="Xml" src="/images/xml.png" />')

        >>> image('rss.png', 'rss syndication')
        literal(u'<img alt="rss syndication" src="/images/rss.png" />')

        >>> image("icon.png", height=16, width=10, alt="Edit Entry")
        literal(u'<img alt="Edit Entry" height="16" src="/images/icon.png" width="10" />')

        >>> image("/icons/icon.gif", width=16, height=16)
        literal(u'<img alt="Icon" height="16" src="/icons/icon.gif" width="16" />')

        >>> image("/icons/icon.gif", width=16)
        literal(u'<img alt="Icon" src="/icons/icon.gif" width="16" />')
        
    """
    options['src'] = compute_public_path(source, 'images')

    if not alt:
        alt = os.path.splitext(os.path.basename(source))[0].title()
    options['alt'] = alt
    
    if width is not None:
        options['width'] = width
    if height is not None:
        options['height'] = height
        
    return HTML.img(**options)

#### Tags for the HTML head

# The absolute path of the WebHelpers javascripts directory
javascript_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'javascripts')

def javascript_link(*sources, **options):
    """Return script include tags for the specified javascript
    ``sources``.
    
    Specify the keyword argument ``defer=True`` to enable the script 
    defer attribute.

    Examples::
    
        >>> print javascript_link('/javascripts/prototype.js', '/other-javascripts/util.js')
        <script src="/javascripts/prototype.js" type="text/javascript"></script>
        <script src="/other-javascripts/util.js" type="text/javascript"></script>

        >>> print javascript_link('/app.js', '/test/test.1.js')
        <script src="/app.js" type="text/javascript"></script>
        <script src="/test/test.1.js" type="text/javascript"></script>
        
    """
    if options.get('defer') == True:
        options['defer'] = 'defer'

    tags = []
    for source in sources:
        content_options = dict(type='text/javascript',
                src=compute_public_path(source, 'javascripts', 'js'))
        content_options.update(options)
        tags.append(HTML.script('',  **content_options))
    return '\n'.join(tags)


def stylesheet_link(*sources, **options):
    """Return CSS link tags for the specified stylesheet ``sources``.

    Each source's URL path is ultimately prepended with the 
    environment's ``SCRIPT_NAME`` (the root path of the web 
    application), unless the URL path is a full-fledged URL 
    (e.g., http://example.com).
    
    Examples::

        >>> stylesheet_link('style.css')
        u'<link href="/stylesheets/style.css" media="screen" rel="Stylesheet" type="text/css" />'

        >>> stylesheet_link('/stylesheets/dir/file.css', media='all')
        u'<link href="/stylesheets/dir/file.css" media="all" rel="Stylesheet" type="text/css" />'

    """
    tag_options = dict(rel='Stylesheet', type='text/css', media='screen')
    tag_options.update(options)
    tag_options.pop('href', None)
    
    tags = [HTML.link(
        **dict(href=compute_public_path(source, 'stylesheets', 'css'), 
               **tag_options)) for source in sources]
    return '\n'.join(tags)


def auto_discovery_link(source, feed_type='rss', **kwargs):
    """Return a link tag allowing auto-detecting of RSS or ATOM feed.
    
    The auto-detection of feed for the current page is only for
    browsers and news readers that support it.

    ``source``
        The URL of the feed. The URL is ultimately prepended with the
        environment's ``SCRIPT_NAME`` (the root path of the web 
        application), unless the URL is fully-fledged 
        (e.g. http://example.com).

    ``feed_type``
        The type of feed. Specifying 'rss' or 'atom' automatically 
        translates to a type of 'application/rss+xml' or 
        'application/atom+xml', respectively. Otherwise the type is
        used as specified. Defaults to 'rss'.
        
    Examples::

        >>> auto_discovery_link('http://feed.com/feed.xml')
        literal(u'<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />')

        >>> auto_discovery_link('http://feed.com/feed.xml', feed_type='atom')
        literal(u'<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />')

        >>> auto_discovery_link('app.rss', feed_type='atom', title='atom feed')
        literal(u'<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />')

        >>> auto_discovery_link('/app.html', feed_type='text/html')
        literal(u'<link href="/app.html" rel="alternate" title="" type="text/html" />')
        
    """
    title = ''
    if feed_type.lower() in ('rss', 'atom'):
        title = feed_type.upper()
        feed_type = 'application/%s+xml' % feed_type.lower()

    tag_args = dict(rel='alternate', type=feed_type, title=title,
                    href=compute_public_path(source))
    kwargs.pop('href', None)
    kwargs.pop('type', None)
    tag_args.update(kwargs)
    return HTML.link(**tag_args)



########## INTERNAL FUNCTIONS ##########

def compute_public_path(source, root_path=None, ext=None):
    """Format the specified source for publishing.
    
    Use the public directory, if applicable.
    
    """
    if ext and not os.path.splitext(os.path.basename(source))[1]:
        source = '%s.%s' % (source, ext)

    # Avoid munging fully-fledged URLs, including 'mailto:'
    parsed = urlparse.urlparse(source)
    if not (parsed[0] and (parsed[1] or parsed[2])):
        # Prefix apps deployed under any SCRIPT_NAME path
        if not root_path or source.startswith('/'):
            source = '%s%s' % (get_script_name(), source)
        else:
            source = '%s/%s/%s' % (get_script_name(), root_path, source)
    return source


def get_script_name():
    """Determine the current web application's ``SCRIPT_NAME``.
    
    .. note::
        This requires Routes to function, and will not pick up the
        SCRIPT_NAME var without it in use.
    
    """
    script_name = ''
    if request_config:
        config = request_config()
        if hasattr(config, 'environ'):
            script_name = config.environ.get('SCRIPT_NAME', '')
    else:
        script_name = ''
    return script_name

